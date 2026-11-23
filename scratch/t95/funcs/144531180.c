__int64 __fastcall sub_144531180(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  __int64 v8; // rbx
  _DWORD v10[10]; // [rsp+20h] [rbp-28h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v10[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v10, 1);
  if ( v7[4] != 0 )
    return 0;
  sub_1408149D0(*a2, v10, a1 + 24);
  if ( v10[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v10, a1 + 32);
  if ( v10[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v10, a1 + 40);
  if ( v10[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v10, a1 + 48);
  if ( v10[0] != 0 )
    return 0;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  sub_14157F990(v10, a2, a1 + 64);
  if ( v10[0] != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
