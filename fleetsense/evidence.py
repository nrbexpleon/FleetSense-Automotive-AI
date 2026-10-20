from __future__ import annotations
import copy,hashlib,hmac,json
from datetime import datetime,timezone

def canonical(value:object)->bytes:return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def create_evidence(report:dict)->dict:
    body={"schema_version":"1.0","generated_at":datetime.now(timezone.utc).isoformat(),"report":copy.deepcopy(report)};return {**body,"integrity":{"algorithm":"sha256","digest":hashlib.sha256(canonical(body)).hexdigest()}}
def verify_evidence(evidence:dict)->bool:
    integrity=evidence.get("integrity",{});body={key:value for key,value in evidence.items() if key not in {"integrity","signature"}};return integrity.get("algorithm")=="sha256" and hmac.compare_digest(integrity.get("digest",""),hashlib.sha256(canonical(body)).hexdigest())
def sign_evidence(evidence:dict,key:bytes)->dict:
    if len(key)<32:raise ValueError("HMAC key must be at least 32 bytes")
    isolated=copy.deepcopy(evidence);return {**isolated,"signature":{"algorithm":"hmac-sha256","value":hmac.new(key,canonical(isolated),hashlib.sha256).hexdigest()}}
def verify_signed_evidence(signed:dict,key:bytes)->bool:
    signature=signed.get("signature",{});evidence={k:v for k,v in signed.items() if k!="signature"};return verify_evidence(evidence) and hmac.compare_digest(signature.get("value",""),hmac.new(key,canonical(evidence),hashlib.sha256).hexdigest())
