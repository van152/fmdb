bool __fastcall sub_143C2D590(__int64 a1)
{
  __int64 v1; // rax
  __int64 v2; // rdx
  unsigned __int64 v3; // rdx
  __int64 v4; // rcx
  _BYTE *i; // rax

  v1 = *(_QWORD *)(a1 + 72);
  v2 = *(_QWORD *)(a1 + 80) - v1;
  if ( v2 == 0 )
    return false;
  v3 = v2 >> 4;
  v4 = 1;
  if ( v3 >= 2 )
    v4 = v3;
  for ( i = (_BYTE *)(v1 + 12); *(i - 1) != 111; i += 16 )
  {
    if ( --v4 == 0 )
      return false;
  }
  return *i == 3;
}
