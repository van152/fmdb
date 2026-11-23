bool __fastcall sub_14386D830(__int64 a1)
{
  int v1; // eax
  char v4; // si
  __int64 v5; // rax
  int v6; // eax
  int v7; // eax

  v1 = *(_DWORD *)(a1 + 52);
  if ( (v1 & 0x40) != 0 )
    return false;
  if ( *(_WORD *)(a1 + 564) == 0xFFFD )
    return sub_1409083C0(a1);
  v4 = 1;
  if ( *(_BYTE *)(a1 + 840) != 3 && *(_QWORD *)(a1 + 920) == 0 && (v1 & 0x20000) == 0 )
  {
    v5 = *(_QWORD *)(a1 + 520);
    if ( v5 == 0 )
      return sub_1409083C0(a1);
    v6 = *(unsigned __int8 *)(v5 + 522);
    if ( v6 != 3 )
    {
      if ( v6 != 1 )
        return sub_1409083C0(a1);
      v7 = *(unsigned __int8 *)(a1 + 572);
      if ( (unsigned int)(v7 - 105) >= 6 && v7 != 8 && (unsigned __int8)sub_1409D5090() == 0 )
        return sub_1409083C0(a1);
    }
  }
  return v4;
}
