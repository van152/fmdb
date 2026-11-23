// THUNK ALIAS -> sub_14386C630 (jmp:0x1409083c0->0x14386c630)
bool __fastcall sub_14386C630(__int64 a1)
{
  int v2; // ecx
  __int64 v3; // rax
  int v4; // edx
  bool result; // al
  int v6; // ecx
  __int64 v7; // rax
  char v8; // cl
  int v9; // edx

  v2 = sub_1400870F0();
  v3 = *(_QWORD *)(a1 + 288);
  if ( v3 != 0 )
    v4 = *(_DWORD *)(v3 + 12);
  else
    v4 = -1;
  result = true;
  if ( v2 != v4 )
  {
    v6 = *(_DWORD *)(a1 + 52);
    result = false;
    if ( (v6 & 0x40) == 0 && *(_BYTE *)(a1 + 840) != 3 && *(_QWORD *)(a1 + 920) == 0 && (v6 & 0x20000) == 0 )
    {
      v7 = *(_QWORD *)(a1 + 520);
      if ( v7 == 0 )
        return *(_WORD *)(a1 + 564) != 0xFFFD;
      v8 = *(_BYTE *)(v7 + 522);
      result = false;
      if ( v8 != 3 && *(_WORD *)(a1 + 564) != 0xFFFD )
      {
        if ( v8 != 1 )
          return true;
        v9 = *(unsigned __int8 *)(a1 + 572);
        result = false;
        if ( (unsigned int)(v9 - 105) >= 6 && v9 != 8 )
          return (unsigned __int8)sub_1409D5090() == 0;
      }
    }
  }
  return result;
}
