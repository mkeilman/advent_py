import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print


class MemorySpace:

    def __init__(self, v, size, num_bytes):
        self.size = size
        self.grid = Day.Grid.grid_of_size(size, size)
        self.byte_coords = self._byte_coords(v)
        n = num_bytes if num_bytes >= 0 else len(self.byte_coords)
        self.bytes = [(x[0], x[1]) for x in self.byte_coords[:n]]
        self.connections = {k:[x for x in v if x not in self.bytes] for k, v in self.grid.coord_neighborhoods.items()}
        self.end_pos = (self.size - 1, self.size - 1)

    def _byte_coords(self, v):
        c = []
        for txt in v:
            c.append([int(x) for x in reversed(re.findall(r"\d+", txt))])
        return c
    
    def display_path(self, path):
        debug_print(self.bytes)
        for r in self.grid.coord_array:
            s = ""
            for c in r:
                if c in self.bytes:
                    s += "#"
                elif c in path:
                    s += "O"
                else:
                    s += "."
            debug_print(s)
        debug_print("")

    def line_path(self, start=(0,0), end=None):
        p = self.grid.line(start, end or self.end_pos, allow_diags=False)
        for b in self.byte_coords:
            bt = (b[0], b[1])
            if bt not in p:
                continue
            i = p.index(bt)
            n = [x for x in self.grid.neighborhood(p[i - 1]) if x not in p]
            debug_print(f"BLOCKED AT {i} {bt} N {n}")
            #for c in p[i + 1:]:
            #    if c not in self.byte_coords:
            #        break
            #else:
            #    return None
            #j = p.index(c)
            p1 = p[:i]
            p2 = p[i + 1:]
            debug_print(f"1 {p1} 2 {p2}")

            #debug_print(f"FIND PATH FROM {p[i - 1]} - {c} {p1} {p2}")
            break
            
        return p
    
    def paths(self):

        def _amend_paths(base_path, unused_connections, depth=0, all_paths=[], rejected_paths=[]):
            debug_print(f"{depth} ALL {len(all_paths)} REJ {len(rejected_paths)} NUM U {len(unused_connections)}")
            n = 0
            ux = [x for x in unused_connections if x in base_path]
            nux = len(ux)
            for pos in ux:
                n += 1
                i = base_path.index(pos)
                #if i + 1 >= _max_path_len(all_paths):
                #    debug_print(f"{depth} INIT PATH TOO LONG {i + 1} >= {_max_path_len(all_paths)}")
                #    break
                initial_path = base_path[:i + 1]
                #debug_print(f"{depth} POS N {n}")
                new_path, u = _path(initial_path, self.end_pos, exclusions={pos: [base_path[i + 1]]}, max_len=_max_path_len(all_paths))
                if not new_path or not u:
                    continue
                if new_path in rejected_paths:
                    debug_print(f"{depth} {n}/{nux} ALREADY REJECTED")
                    continue
                if new_path in all_paths:
                    debug_print(f"{depth} {n}/{nux} ALREADY ADDED")
                    continue
                #if new_path not in all_paths:
                if len(new_path) < _max_path_len(all_paths):
                    #debug_print(f"{depth} OK TO ADD NEW {len(new_path)} < {_max_path_len(all_paths)}")
                    self.display_path(new_path)
                    all_paths.append(new_path)
                #debug_print(f"{depth} ADD NEW {len(new_path)} MAX {_max_path_len(all_paths)}")
                else:
                    debug_print(f"{depth} {n}/{nux} TOO LONG {len(new_path)} >= {_max_path_len(all_paths)}")
                    rejected_paths.append(new_path)
                uu = [x for x in u if x in new_path and new_path.index(x) + 1 < _max_path_len(all_paths)]
                if not uu:
                    debug_print(f"{depth} {n}/{nux} NO UNUSED")
                    continue
                _amend_paths(new_path, uu, depth=depth + 1, all_paths=all_paths, rejected_paths=rejected_paths)
            debug_print(f"{depth} {n}/{nux} DONE AMEND")
            return

        def _exclude(pos, connection, exclusions):
            if not exclusions.get(pos):
                exclusions[pos] = []
            exclusions[pos].append(connection)
        
        def _conn(pos, path, exclusions={}, unused={}):
            return [x for x in self.connections[pos] if x != path[path.index(pos) - 1] and x not in path and x not in exclusions.get(pos, [])]

        def _max_path_len(paths):
            return min([len(x) for x in paths])

        def _path(initial_path, end_pos, exclusions={}, max_len=1e26):
            pos0 = initial_path[-1]
            pos = pos0
            pp = initial_path[:]
            done = False
            unused = {}
            while not done and pos != end_pos:
                if len(pp) >= max_len:
                    #debug_print(f"TOO LONG FROM {pos} - {pp[-1]}: {len(pp)}")
                    pos = _trim_to_prev_branch(pp, exclusions, limit=pos)
                    #debug_print(f"TRIMMED TO {pos} L {len(pp)}")
                    if pos is None:
                        break
                # loop through the connections to this position, not counting
                # the preivous position and excluded positions
                p_con = _conn(pos, pp, exclusions=exclusions)
                for p in p_con:
                    pp.append(p)
                    u = [x for x in p_con if x != p]
                    if u:
                        unused[pos] = u
                    pos = p
                    break
                else:
                    #debug_print(f"NO BRANCH: {pos}")
                    pos = _trim_to_prev_branch(pp, exclusions, limit=pos0)
                    done = not pos

            if pos != end_pos:
                return [], None
            if pp == initial_path:
                debug_print("SAME??")
                #return [], None
            return pp, unused

        def _prev_branch(path, exclusions={}, limit=None):
            i = -1
            q = path[i]
            c = _conn(q, path, exclusions=exclusions)
            while not len(c):
                if i == -len(path):
                    return None
                i -= 1
                q = path[i]
                if limit and q == limit and q != path[0]:
                    return None
                c = _conn(q, path, exclusions=exclusions)
            return q
        

        def _trim(arr, n):
            for _ in range(n):
                arr.pop()

        def _trim_to_pos(pos, path, exlcusions):
            n = len(path) - path.index(pos) - 1
            for i in range(n):
                # exclude intervening postions if they have no valid connections
                _exclude(path[-i - 2], path[-i - 1], exlcusions)
            _trim(path, n)


        def _trim_to_prev_branch(path, exclusions, limit=None):
            q = _prev_branch(path, exclusions=exclusions, limit=limit)
            if q:
                _trim_to_pos(q, path, exclusions)
            return q


        start = (0, 0)

        paths = []
        path, unused = _path([start], self.end_pos)
        debug_print(f"FIRST L {len(path)}")
        #self.display_path(path)
        paths.append(path)
        _amend_paths(path, unused, all_paths=paths)
        return paths

class AdventDay(Day.Base):

    TEST = [
        "5,4",
        "4,2",
        "4,5",
        "3,0",
        "2,1",
        "6,3",
        "2,4",
        "1,5",
        "0,6",
        "3,3",
        "2,6",
        "5,1",
        "1,2",
        "5,5",
        "2,5",
        "6,5",
        "1,4",
        "0,4",
        "6,4",
        "1,1",
        "6,1",
        "1,0",
        "0,5",
        "1,6",
        "2,0",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 18)
        self.args_parser.add_argument(
            "--num-bytes",
            type=int,
            help="number of fallen bytes",
            default=0,
            dest="num_bytes",
        )
        self.args_parser.add_argument(
            "--size",
            type=int,
            help="size of memory space",
            default=7,
            dest="size",
        )
        self.add_args(run_args)
       

    def run(self):
        m = MemorySpace(self.input, self.size, self.num_bytes)
        #paths = m.paths()
        #pr = sorted(paths, key=lambda x: len(x))
        #debug_print(f"FOUND {len(paths)} PATHS LENS {[len(x) for x in pr]}")
        #debug_print(f"SHORTEST NUM STEPS {len(pr[0]) - 1}")
        #m.display_path(pr[0])
        m.display_path(m.line_path())
