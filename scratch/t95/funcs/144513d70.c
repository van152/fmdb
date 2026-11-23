bool __fastcall sub_144513D70(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rsi
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbx
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // rsi
  __int64 v16; // rsi
  _DWORD *v17; // rbx
  __int64 v18; // rax
  int v19; // eax
  _DWORD *v20; // rbx
  __int64 v21; // rax
  int v22; // eax
  __int64 v23; // rsi
  __int64 v24; // rsi
  _DWORD *v25; // rbx
  __int64 v26; // rax
  int v27; // eax
  __int64 v28; // rsi
  _DWORD *v29; // rbx
  __int64 v30; // rax
  int v31; // eax
  __int64 v32; // rsi
  __int64 v33; // rsi
  _DWORD *v34; // rdi
  __int64 v35; // rdx
  _DWORD v36[9]; // [rsp+24h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v36[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v36, 1);
  if ( v7[4] != 0 )
    return false;
  if ( a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 24);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    v36[0] = v11;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v36, 4);
    if ( v9[4] != 0 )
      return false;
    v12 = (_DWORD *)*a2;
    v13 = *(_QWORD *)(a1 + 32);
    v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
    v36[0] = v14;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v12 + 40LL))(v12, v36, 4);
    if ( v12[4] != 0 )
      return false;
    v15 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 72, 2);
    if ( v15[4] != 0 )
      return false;
    v16 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 74, 2);
    if ( *(_DWORD *)(v16 + 16) != 0 )
      return false;
    v17 = (_DWORD *)*a2;
    v18 = *(_QWORD *)(a1 + 48);
    v19 = v18 != 0 ? *(_DWORD *)(v18 + 8) : -1;
    v36[0] = v19;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, v36, 4);
    if ( v17[4] != 0 )
      return false;
    v20 = (_DWORD *)*a2;
    v21 = *(_QWORD *)(a1 + 56);
    v22 = v21 != 0 ? *(_DWORD *)(v21 + 8) : -1;
    v36[0] = v22;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v20 + 40LL))(v20, v36, 4);
    if ( v20[4] != 0 )
      return false;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 76, 1);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return false;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 77, 1);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return false;
    v25 = (_DWORD *)*a2;
    v26 = *(_QWORD *)(a1 + 40);
    v27 = v26 != 0 ? *(_DWORD *)(v26 + 8) : -1;
    v36[0] = v27;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v25 + 40LL))(v25, v36, 4);
    if ( v25[4] != 0 )
      return false;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 78, 1);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return false;
    v29 = (_DWORD *)*a2;
    v30 = *(_QWORD *)(a1 + 64);
    v31 = v30 != 0 ? *(_DWORD *)(v30 + 8) : -1;
    v36[0] = v31;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v29 + 40LL))(v29, v36, 4);
    if ( v29[4] != 0 )
      return false;
  }
  v32 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v32 + 16) != 0 )
    return false;
  v33 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v33 + 16) != 0 )
    return false;
  v34 = (_DWORD *)*a2;
  v35 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v34 + 40LL))(v34, v35, 4);
  return v34[4] == 0;
}
