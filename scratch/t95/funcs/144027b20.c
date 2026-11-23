__int64 __fastcall sub_144027B20(__int64 a1, char a2)
{
  __int64 v2; // r8
  unsigned __int64 v3; // rcx
  __int64 v4; // rcx
  __int64 v5; // rdx
  __int64 v6; // rcx
  __int64 v7; // r10
  bool v8; // cc
  __int64 result; // rax
  unsigned __int64 v10; // r11
  __int64 v11; // rdx
  __int64 v12; // rcx
  __int64 v13; // r10
  unsigned __int64 v14; // r11

  v2 = *(_QWORD *)(a1 + 24);
  v3 = (unsigned __int64)(*(_QWORD *)(a1 + 32) - v2) >> 3;
  if ( (int)v3 <= 0 )
    return 0;
  v4 = (unsigned int)(v3 - 1);
  if ( a2 != 0 )
  {
    v5 = v4 + 1;
    v6 = v4 << 56;
    v7 = 0x220263E00LL;
    while ( 1 )
    {
      result = *(_QWORD *)(v2 + (v6 >> 53));
      if ( result != 0 )
      {
        v10 = (unsigned int)*(char *)(result + 40);
        if ( (unsigned int)v10 <= 0x21 && _bittest64(&v7, v10) && (*(_BYTE *)(result + 176) & 1) == 0 )
          break;
      }
      v6 -= 0x100000000000000LL;
      v8 = v5-- <= 1;
      if ( v8 )
        return 0;
    }
  }
  else
  {
    v11 = v4 + 1;
    v12 = v4 << 56;
    v13 = 0x220263E00LL;
    while ( 1 )
    {
      result = *(_QWORD *)(v2 + (v12 >> 53));
      if ( result != 0 )
      {
        v14 = (unsigned int)*(char *)(result + 40);
        if ( (unsigned int)v14 <= 0x21 )
        {
          if ( _bittest64(&v13, v14) )
            break;
        }
      }
      v12 -= 0x100000000000000LL;
      v8 = v11-- <= 1;
      if ( v8 )
        return 0;
    }
  }
  return result;
}
