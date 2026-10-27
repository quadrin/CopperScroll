"""Recover complete local ZIP members when a saved archive lacks its directory.

Require complete local members, supported compression, and matching CRC/size.
Preserve the original. This utility reads bytes and never renders source images.
"""
import argparse,binascii,hashlib,json,pathlib,struct,zipfile,zlib

def repair(source,output,receipt):
    data=source.read_bytes();off=0;members=[]
    if output.exists():raise FileExistsError(output)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_STORED) as archive:
        while data[off:off+4]==b'PK\x03\x04':
            _,version,flag,method,tm,dt,crc,csize,usize,nlen,xlen=struct.unpack_from('<IHHHHHIIIHH',data,off)
            if flag & (1|8):raise ValueError('Encrypted or descriptor-based member unsupported')
            name=data[off+30:off+30+nlen].decode('utf8');start=off+30+nlen+xlen;end=start+csize
            if method not in (0,8) or end>len(data):raise ValueError('Unsupported or truncated member: '+name)
            payload=zlib.decompress(data[start:end],-15) if method==8 else data[start:end]
            if len(payload)!=usize or binascii.crc32(payload)&0xffffffff!=crc:raise ValueError('CRC/size failed: '+name)
            if name in {m['member'] for m in members}:raise ValueError('Duplicate member: '+name)
            archive.writestr(name,payload)
            members.append({'member':name,'bytes':usize,'sha256':hashlib.sha256(payload).hexdigest(),'source_crc32':f'{crc:08x}'})
            off=end
        if off!=len(data):raise ValueError('Unparsed trailing bytes; do not claim complete recovery')
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None or len(archive.namelist())!=len(members):raise ValueError('Rebuilt ZIP failed validation')
        for member in members:
            if hashlib.sha256(archive.read(member['member'])).hexdigest()!=member['sha256']:raise ValueError('Rebuilt hash mismatch')
    result={'original_sha256':hashlib.sha256(data).hexdigest(),'original_bytes':len(data),'original_has_central_directory':False,'recovered_complete_member_count':len(members),'unparsed_bytes':len(data)-off,'repaired_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'repaired_bytes':output.stat().st_size,'members':members}
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='members'}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=pathlib.Path);parser.add_argument('output',type=pathlib.Path);parser.add_argument('receipt',type=pathlib.Path)
    a=parser.parse_args();repair(a.source,a.output,a.receipt)
