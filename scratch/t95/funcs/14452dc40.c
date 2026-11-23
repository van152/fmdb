__int64 __fastcall sub_14452DC40(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
  __int64 v12; // rax
  int v13; // eax
  _DWORD v15[10]; // [rsp+20h] [rbp-28h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v15[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v15, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = *(_QWORD *)(a1 + 24);
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v15[0] = v10;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v15, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  v12 = *(_QWORD *)(a1 + 64);
  v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
  v15[0] = v13;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, v15, 4);
  if ( v11[4] != 0 )
    return 0;
  sub_1408149D0(*a2, v15, a1 + 32);
  if ( v15[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v15, a1 + 40);
  if ( v15[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v15, a1 + 48);
  if ( v15[0] != 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB89D0(a1 + 56, a2) == 0 )
    return 0;
  sub_14157F240(v15, a2, a1 + 72);
  if ( v15[0] != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
