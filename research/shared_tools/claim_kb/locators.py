"""Resolve a public record's bounded metadata locator; never serve arbitrary paths."""
import csv
import io
import json
import re
from urllib.parse import quote
from .model import public_view


def resolve(data,root,address,number,base_commit):
    by={r['key']:r for r in public_view(data)['records']}
    if address not in by:raise ValueError('Unknown or unavailable record')
    record=by[address]
    if number<0 or number>=len(record['locators']):raise ValueError('Unknown locator')
    loc=record['locators'][number];path=loc['repo_path'];pointer=loc['pointer']
    result={'record_key':address,'locator':loc,
            'repository_url':'https://github.com/quadrin/CopperScroll/blob/'+base_commit+'/'+quote(path,safe='/'),
            'source_citation':record['payload'].get('citation'),
            'scope':'Recorded metadata only. Original source assets stay in their established locations.'}
    if path not in data['inputs'] or not (root/path).is_file():
        result['gap']='Source pointer preserved; this source is not a materialized pilot input.'
        return result
    if (root/path).resolve().is_relative_to(root.resolve()) is False:raise ValueError('Path escapes repository')
    # Whole-file raw exports could expose private neighboring records. Text notes
    # retain their citation/pointer and an explicit repository link instead.
    if pointer=='/' or not path.endswith(('.json','.csv')):
        result['recorded_metadata']=record['payload']
        return result
    text=(root/path).read_text(encoding='utf-8-sig')
    data_value=json.loads(text) if path.endswith('.json') else list(csv.DictReader(io.StringIO(text)))
    selectors=re.findall(r'/([\w]+)=(.*?)(?=/[\w]+=|$)',pointer)
    if selectors:
        if not isinstance(data_value,list):
            result['gap']='Named selector belongs to a generated projection; follow the canonical record pointer.'
            return result
        filters=dict(selectors)
        if filters.get('branch','').startswith('regional:'):
            _,branch,orientation,ruleset=filters.pop('branch').split(':')
            filters.update(branch=branch,orientation=orientation,ruleset=ruleset)
        matched=[r for r in data_value if all(str(r.get(k))==v for k,v in filters.items())]
        if not matched:raise ValueError('Unresolved source selector: '+pointer)
        result['source_record']=matched
    else:
        try:
            for token in pointer.lstrip('/').split('/'):
                token=token.replace('~1','/').replace('~0','~')
                data_value=data_value[int(token)] if isinstance(data_value,list) else data_value[token]
        except (ValueError,IndexError,KeyError,TypeError):
            result['gap']='Generated projection locator; canonical record and its exact source citation remain available.'
            return result
        result['source_record']=data_value
    return result
