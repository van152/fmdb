// THUNK ALIAS -> sub_14420F9B0 (jmp:0x1413360c0->0x14420f9b0)
unsigned int *__fastcall sub_14420F9B0(__int64 a1, unsigned int *a2, _DWORD *a3)
{
  char v5; // al
  unsigned int v6; // ecx

  if ( *(_QWORD *)a3 == a1 )
  {
    v6 = a3[2];
  }
  else
  {
    v5 = (*(__int64 (__fastcall **)(_QWORD, _DWORD *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3);
    v6 = 0;
    if ( v5 == 4 )
      v6 = a3[2] & 0xFF000000 | ((unsigned __int8)a3[2] << 16) | a3[2] & 0xFF00 | (unsigned __int8)BYTE2(a3[2]);
  }
  *a2 = v6;
  return a2;
}
