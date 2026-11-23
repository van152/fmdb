// THUNK ALIAS -> sub_1438AACD0 (jmp:0x140968430->0x1438aacd0)
__int64 __fastcall sub_1438AACD0(__int64 a1)
{
  unsigned int v1; // esi
  __int64 v2; // rax
  int v3; // eax
  int v4; // eax

  LOBYTE(v1) = 1;
  if ( *(_BYTE *)(a1 + 840) != 3 && *(_QWORD *)(a1 + 920) == 0 && (*(_BYTE *)(a1 + 54) & 2) == 0 )
  {
    if ( *(_WORD *)(a1 + 564) == 0xFFFD )
      return 0;
    v2 = *(_QWORD *)(a1 + 520);
    if ( v2 == 0 )
      return 0;
    v3 = *(unsigned __int8 *)(v2 + 522);
    if ( v3 != 3 )
    {
      if ( v3 != 1 )
        return 0;
      v4 = *(unsigned __int8 *)(a1 + 572);
      if ( (unsigned int)(v4 - 105) >= 6 && v4 != 8 && (unsigned __int8)sub_1409D5090() == 0 )
        return 0;
    }
  }
  return v1;
}
