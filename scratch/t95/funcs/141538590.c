bool __fastcall sub_141538590(__int64 a1, _QWORD *a2, __int64 a3, char a4)
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
  _DWORD *v20; // rbx
  __int64 v21; // rax
  int v22; // eax
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  __int64 v34; // rsi
  __int64 v35; // rsi
  __int64 v36; // rsi
  _DWORD *v37; // rdi
  __int64 v38; // rdx
  _DWORD v39[9]; // [rsp+24h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v39[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v39, 1);
  if ( v7[4] != 0 )
    return false;
  if ( a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 24);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    v39[0] = v11;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v39, 4);
    if ( v9[4] != 0 )
      return false;
    v12 = (_DWORD *)*a2;
    v13 = *(_QWORD *)(a1 + 32);
    v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
    v39[0] = v14;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v12 + 40LL))(v12, v39, 4);
    if ( v12[4] != 0 )
      return false;
    v15 = (_DWORD *)*a2;
    v16 = *(_QWORD *)(a1 + 40);
    v17 = v16 != 0 ? *(_DWORD *)(v16 + 8) : -1;
    v39[0] = v17;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v15 + 40LL))(v15, v39, 4);
    if ( v15[4] != 0 )
      return false;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 48, a2) == 0 )
      return false;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 52, a2) == 0 )
      return false;
    v18 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 60, 4);
    if ( v18[4] != 0 )
      return false;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 100, 1);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return false;
    v20 = (_DWORD *)*a2;
    v21 = *(_QWORD *)(a1 + 72);
    v22 = v21 != 0 ? *(_DWORD *)(v21 + 8) : -1;
    v39[0] = v22;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v20 + 40LL))(v20, v39, 4);
    if ( v20[4] != 0 )
      return false;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 101, 1);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return false;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 64, 4);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return false;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 80, 4);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return false;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 4);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return false;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 88, 4);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return false;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 92, 4);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return false;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 56, a2) == 0 )
      return false;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 102, 1);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return false;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 96, 4);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return false;
    v31 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 105, 1);
    if ( *(_DWORD *)(v31 + 16) != 0 )
      return false;
    v32 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 103, 1);
    if ( *(_DWORD *)(v32 + 16) != 0 )
      return false;
    v33 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 104, 1);
    if ( *(_DWORD *)(v33 + 16) != 0 )
      return false;
    v34 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 68, 4);
    if ( *(_DWORD *)(v34 + 16) != 0 )
      return false;
  }
  v35 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v35 + 16) != 0 )
    return false;
  v36 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v36 + 16) != 0 )
    return false;
  v37 = (_DWORD *)*a2;
  v38 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v37 + 40LL))(v37, v38, 4);
  return v37[4] == 0;
}
