// THUNK ALIAS -> sub_1439C52A0 (jmp:0x140af87d0->0x1439c52a0)
__int64 __fastcall sub_1439C52A0(__int64 a1)
{
  __int64 v1; // rax
  __int64 v2; // rax
  __int64 v3; // rax
  char v4; // cl
  __int64 v5; // rdx
  __int64 result; // rax

  v1 = *(_QWORD *)(a1 + 216);
  if ( v1 == 0 )
    return 0;
  v2 = *(_QWORD *)(v1 + 240);
  if ( v2 == 0 )
    return 0;
  v3 = *(_QWORD *)(v2 + 96);
  if ( v3 == 0 )
    return 0;
  v4 = *(_BYTE *)(a1 + 185);
  if ( v4 != 0 )
  {
    v5 = *(_QWORD *)(v3 + 624);
    if ( v5 == 0 )
      return 0;
  }
  else
  {
    v5 = *(_QWORD *)(v3 + 624);
  }
  result = v3 + 88;
  if ( v4 != 0 )
    return v5;
  return result;
}
