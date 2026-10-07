"""Minimal decoder for SvelteKit devalue-encoded __data.json payloads."""
import json, sys

def unflatten(arr):
    cache = {}
    def h(i):
        if isinstance(i, int):
            if i == -1: return None
            if i in cache: return cache[i]
            v = arr[i]
            if isinstance(v, dict):
                out = {}
                cache[i] = out
                for k, j in v.items():
                    out[k] = h(j)
                return out
            if isinstance(v, list):
                if v and isinstance(v[0], str) and v[0] in ('Date','Set','Map','BigInt','RegExp','null'):
                    return v
                out = []
                cache[i] = out
                for j in v:
                    out.append(h(j))
                return out
            cache[i] = v
            return v
        return i
    return h(0)

def load(path):
    d = json.load(open(path, encoding='utf8'))
    res = []
    for node in d.get('nodes', []):
        if node and node.get('type') == 'data':
            res.append(unflatten(node['data']))
    return res

if __name__ == '__main__':
    r = load(sys.argv[1])
    for n in r:
        print(json.dumps(n, ensure_ascii=False)[:3000])
