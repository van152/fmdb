__int64 __fastcall sub_143C113C0(_QWORD *a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  _DWORD *v12; // r14
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // r14
  __int64 v16; // rax
  int v17; // eax
  __int64 v18; // rbx
  __int64 v19; // rbx
  _DWORD *v20; // r14
  __int64 v21; // rax
  int v22; // eax
  _DWORD *v23; // r14
  __int64 v24; // rax
  int v25; // eax
  __int64 v26; // rbx
  _DWORD v28[11]; // [rsp+2Ch] [rbp-2Ch] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v28[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v28, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 83, 1);
  if ( v8[4] != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 9, 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 76, 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 84, 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  v13 = a1[4];
  v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
  v28[0] = v14;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v12 + 40LL))(v12, v28, 4);
  if ( v12[4] != 0 )
    return 0;
  v15 = (_DWORD *)*a2;
  v16 = a1[5];
  v17 = v16 != 0 ? *(_DWORD *)(v16 + 8) : -1;
  v28[0] = v17;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v15 + 40LL))(v15, v28, 4);
  if ( v15[4] != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 10, 2);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 82, 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = (_DWORD *)*a2;
  v21 = a1[6];
  v22 = v21 != 0 ? *(_DWORD *)(v21 + 8) : -1;
  v28[0] = v22;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v20 + 40LL))(v20, v28, 4);
  if ( v20[4] != 0 )
    return 0;
  v23 = (_DWORD *)*a2;
  v24 = a1[7];
  v25 = v24 != 0 ? *(_DWORD *)(v24 + 8) : -1;
  v28[0] = v25;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v23 + 40LL))(v23, v28, 4);
  if ( v23[4] != 0 )
    return 0;
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 85, 1);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
