// THUNK ALIAS -> sub_143C94430 (jmp:0x140ebb440->0x143c94430)
__int64 __fastcall sub_143C94430(__int64 a1, char a2)
{
  __int64 v2; // rax
  int v4; // esi
  __int64 v5; // rdx
  __int64 v6; // rax
  __int64 result; // rax
  int v8; // ecx

  v2 = *(_QWORD *)(a1 + 96);
  if ( v2 == 0 )
    return 0;
  v4 = a1;
  if ( *(_BYTE *)(a1 + 245) == 0 || (v5 = *(_QWORD *)(v2 + 272)) == 0 )
  {
    v5 = *(_QWORD *)(v2 + 264);
    if ( v5 == 0 )
      return 0;
  }
  v6 = sub_1408B4CB0(qword_141B5AD60, *(_QWORD *)(v5 + 368), *(unsigned __int8 *)(v5 + 185));
  if ( v6 == 0 )
    return 0;
  result = sub_140D83E70(v6, v4, (unsigned int)&dword_141AAE084, 0, 0, a2);
  if ( result == 0 )
    return 0;
  v8 = *(unsigned __int8 *)(result + 86);
  if ( v8 == 26 || v8 == 13 )
    return 0;
  return result;
}
