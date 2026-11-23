__int64 __fastcall sub_140FFF480(_QWORD *a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // r14
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // r14
  __int64 v12; // rax
  int v13; // eax
  _DWORD *v14; // r14
  __int64 v15; // rax
  int v16; // eax
  _DWORD *v17; // r14
  __int64 v18; // rax
  int v19; // eax
  __int64 v20; // rbx
  _DWORD *v21; // r14
  __int64 v22; // rax
  int v23; // eax
  __int64 v25; // rbx
  __int64 v26; // rbx
  __int64 v27; // rbx
  __int64 v28; // rbx
  __int64 v29; // rbx
  __int64 v30; // rbx
  __int64 v31; // rbx
  __int64 v32; // rbx
  __int64 v33; // rbx
  __int64 v34; // rbx
  __int64 v35; // rbx
  _DWORD v36[12]; // [rsp+28h] [rbp-30h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v36[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v36, 1);
  if ( v7[4] != 0 )
    return 0;
  sub_1408149D0(*a2, v36, a1 + 3);
  if ( v36[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v36, a1 + 4);
  if ( v36[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v36, a1 + 5);
  if ( v36[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v36, a1 + 6);
  if ( v36[0] != 0 || (unsigned __int8)sub_140DB89D0(a1 + 12, a2) == 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = a1[8];
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v36[0] = v10;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v36, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  v12 = a1[9];
  v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
  v36[0] = v13;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, v36, 4);
  if ( v11[4] != 0 )
    return 0;
  v14 = (_DWORD *)*a2;
  v15 = a1[10];
  v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
  v36[0] = v16;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v14 + 40LL))(v14, v36, 4);
  if ( v14[4] != 0 )
    return 0;
  v17 = (_DWORD *)*a2;
  v18 = a1[11];
  v19 = v18 != 0 ? *(_DWORD *)(v18 + 8) : -1;
  v36[0] = v19;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, v36, 4);
  if ( v17[4] != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 100, 4);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = (_DWORD *)*a2;
  v22 = a1[13];
  v23 = v22 != 0 ? *(_DWORD *)(v22 + 8) : -1;
  v36[0] = v23;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v21 + 40LL))(v21, v36, 4);
  if ( v21[4] != 0 )
    return 0;
  if ( (_BYTE)a4 != 0 )
  {
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 14, 2);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return 0;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 114, 2);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return 0;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 116, 2);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return 0;
  }
  v28 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 118, 1);
  if ( *(_DWORD *)(v28 + 16) != 0 )
    return 0;
  v29 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 119, 1);
  if ( *(_DWORD *)(v29 + 16) != 0 )
    return 0;
  v30 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 15, 1);
  if ( *(_DWORD *)(v30 + 16) != 0 )
    return 0;
  v31 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 121, 1);
  if ( *(_DWORD *)(v31 + 16) != 0 )
    return 0;
  v32 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 122, 1);
  if ( *(_DWORD *)(v32 + 16) != 0 )
    return 0;
  v33 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 123, 1);
  if ( *(_DWORD *)(v33 + 16) != 0 )
    return 0;
  v34 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 124, 1);
  if ( *(_DWORD *)(v34 + 16) != 0 )
    return 0;
  v35 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 125, 1);
  if ( *(_DWORD *)(v35 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
