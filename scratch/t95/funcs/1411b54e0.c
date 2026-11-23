// THUNK ALIAS -> sub_143FF5180 (jmp:0x1411b54e0->0x143ff5180)
char __fastcall sub_143FF5180(__int64 a1)
{
  __int64 v1; // rdx
  __int64 v2; // rax
  __int16 *v3; // rcx
  int v4; // eax
  __int16 v5; // cx
  char result; // al

  v1 = 368;
  if ( *(_BYTE *)(a1 + 47) == 0 )
    v1 = 216;
  if ( *(_QWORD *)(*(_QWORD *)(a1 + 48) + v1) == 0 )
    return -1;
  v2 = *(_QWORD *)(a1 + 160);
  v3 = (__int16 *)(a1 + 168);
  if ( v2 != 0 )
    v3 = (__int16 *)(v2 + 248);
  v4 = (int)(float)((float)((float)*v3 * MEMORY[0x14187CCF8]) + MEMORY[0x141775530]);
  v5 = 11;
  if ( (__int16)v4 >= 12 )
    v5 = v4;
  result = 20;
  if ( v5 < 20 )
    return v5;
  return result;
}
