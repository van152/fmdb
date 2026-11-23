__int64 __fastcall sub_143EC0D40(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  _DWORD *v14; // r14
  __int64 v15; // rax
  int v16; // eax
  __int64 v17; // rbx
  char v19; // [rsp+27h] [rbp-31h] BYREF
  int v20; // [rsp+28h] [rbp-30h] BYREF
  _DWORD v21[11]; // [rsp+2Ch] [rbp-2Ch] BYREF

  v7 = (_DWORD *)*a2;
  v19 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v19, 1);
  if ( v7[4] != 0 )
    return 0;
  sub_1408149D0(*a2, &v20, a1 + 24);
  if ( v20 != 0 )
    return 0;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 58, 1);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 59, 1);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 60, 1);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 2);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 54, 2);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 2);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = (_DWORD *)*a2;
  v15 = *(_QWORD *)(a1 + 40);
  v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
  v21[0] = v16;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v14 + 40LL))(v14, v21, 4);
  if ( v14[4] != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 4);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
