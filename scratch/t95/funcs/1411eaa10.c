// THUNK ALIAS -> sub_144028350 (jmp:0x1411eaa10->0x144028350)
__int64 __fastcall sub_144028350(__int64 a1, char a2, int a3, int a4)
{
  __int64 v4; // rdi
  __int64 v9; // rdi
  __int64 v10; // rbp

  v4 = *(_QWORD *)(*(_QWORD *)(a1 + 176) + 8LL) - **(_QWORD **)(a1 + 176);
  if ( v4 == 0 )
    return 0;
  v9 = v4 >> 3;
  while ( 1 )
  {
    v10 = *(_QWORD *)(**(_QWORD **)(a1 + 176) + 8 * v9 - 8);
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v10 + 56LL))(v10) == a2
      && (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v10 + 64LL))(v10) == a3
      && (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)v10 + 72LL))(v10) == a4 )
    {
      break;
    }
    if ( --v9 == 0 )
      return 0;
  }
  return v10;
}
