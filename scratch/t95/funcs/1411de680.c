// THUNK ALIAS -> sub_144018060 (jmp:0x1411de680->0x144018060)
int *__fastcall sub_144018060(__int64 a1, int *a2)
{
  __int64 v4; // rdi
  __int64 v5; // rax
  int v6; // ecx

  do
  {
    v4 = a1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60) != 0 )
      break;
    if ( *(_BYTE *)(v4 + 186) != 0 )
      break;
    a1 = sub_140E75FF0(v4, 0);
    if ( a1 == 0 )
      break;
  }
  while ( a1 != v4 );
  v5 = *(_QWORD *)(v4 + 176);
  if ( v5 != 0 && (v6 = *(_DWORD *)(v5 + 160)) != 0 && *(_DWORD *)(v5 + 168) != v6 )
    *a2 = v6;
  else
    sub_1411DF450(v4, a2, 0, 3, 0, 1u, 0);
  return a2;
}
