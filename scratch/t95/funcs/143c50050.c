__int64 __fastcall sub_143C50050(__int64 a1, __int64 a2, int a3)
{
  __int64 v3; // rsi
  __int64 v4; // rax
  unsigned __int64 v5; // rax
  __int64 v6; // rcx
  _BYTE *v7; // rsi
  __int64 result; // rax
  __int64 v9; // rsi

  v3 = *(_QWORD *)(a1 + 72);
  v4 = *(_QWORD *)(a1 + 80) - v3;
  if ( v4 == 0 )
    return 0;
  v5 = v4 >> 4;
  v6 = 1;
  if ( v5 >= 2 )
    v6 = v5;
  v7 = (_BYTE *)(v3 + 11);
  result = 0;
  while ( *v7 != 55 )
  {
    v7 += 16;
    if ( --v6 == 0 )
      return result;
  }
  result = 0;
  if ( *(v7 - 1) == 1 )
  {
    v9 = *(_QWORD *)(v7 - 11);
    if ( v9 != 0 )
    {
      if ( a3 > 19 )
        return v9;
      if ( (_BYTE)a2 == 0 )
        return v9;
      LOBYTE(a2) = 1;
      result = sub_140E759F0(v9, a2, (unsigned int)(a3 + 1));
      if ( result == 0 )
        return v9;
    }
  }
  return result;
}
