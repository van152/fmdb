bool __fastcall sub_143FD0C30(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rsi
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbx
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // rbx
  __int64 v16; // rax
  int v17; // eax
  _DWORD *v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  _DWORD *v31; // rdi
  __int64 v32; // rdx
  char v33; // [rsp+2Bh] [rbp-2Dh] BYREF
  int v34; // [rsp+2Ch] [rbp-2Ch] BYREF
  int v35; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v36[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v33 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v33, 1);
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
    v35 = v14;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v12 + 40LL))(v12, &v35, 4);
    if ( v12[4] != 0 )
      return false;
    v15 = (_DWORD *)*a2;
    v16 = *(_QWORD *)(a1 + 40);
    v17 = v16 != 0 ? *(_DWORD *)(v16 + 8) : -1;
    v34 = v17;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v15 + 40LL))(v15, &v34, 4);
    if ( v15[4] != 0 )
      return false;
    v18 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 54, 2);
    if ( v18[4] != 0 )
      return false;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 57, 1);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return false;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 58, 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return false;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 59, 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      return false;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 60, 1);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      return false;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 61, 1);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return false;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 2);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return false;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 50, 2);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return false;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 2);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return false;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 1);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return false;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 62, 1);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return false;
  }
  v29 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v29 + 16) != 0 )
    return false;
  v30 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v30 + 16) != 0 )
    return false;
  v31 = (_DWORD *)*a2;
  v32 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v31 + 40LL))(v31, v32, 4);
  return v31[4] == 0;
}
