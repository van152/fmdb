// THUNK ALIAS -> sub_1439C76C0 (jmp:0x140af9070->0x1439c76c0)
__int16 *__fastcall sub_1439C76C0(__int16 *a1, __int64 a2)
{
  __int16 v2; // di
  int v4; // r8d
  __int16 v5; // cx
  __int16 v6; // ax
  unsigned __int16 v7; // di
  __int16 v8; // dx

  v2 = a2;
  a1[1] = a2;
  *a1 = 1;
  LOBYTE(a2) = 7;
  sub_140051EE0(a1, a2);
  v4 = (unsigned __int16)a1[1];
  if ( (_WORD)v4 == v2 )
  {
    if ( v2 != 2000 )
    {
      v5 = *a1;
      v6 = (*a1 & 0x1FF) - 8;
      if ( (*a1 & 0x1FFu) < 8 )
      {
        v7 = v2 - 1;
        v8 = 3;
        if ( (unsigned __int16)(23593 * v7) < 0xA3Eu )
          v8 = 15;
        v4 = v7;
        v6 += ((unsigned __int16)(v7 & v8) == 0) + 365;
      }
      goto LABEL_10;
    }
  }
  else if ( v2 != 2000 )
  {
    v5 = *a1;
    if ( (*a1 & 0x1FF) == 0x16E )
    {
      v6 = 358;
LABEL_10:
      *(_DWORD *)a1 = (v4 << 16) | (unsigned __int16)((v6 + 1) | v5 & 0xFE00);
    }
  }
  return a1;
}
