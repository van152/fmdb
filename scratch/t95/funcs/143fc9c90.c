__int64 __fastcall sub_143FC9C90(_QWORD *a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbx
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // rbx
  __int64 v16; // rax
  int v17; // eax
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rbx
  __int64 v24; // rbx
  char v26; // [rsp+2Bh] [rbp-2Dh] BYREF
  int v27; // [rsp+2Ch] [rbp-2Ch] BYREF
  int v28; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v29[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v26 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v26, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 68, 1);
  if ( v8[4] != 0 )
    return 0;
  v9 = (_DWORD *)*a2;
  v10 = a1[3];
  v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
  v29[0] = v11;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v29, 4);
  if ( v9[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  v13 = a1[4];
  v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
  v28 = v14;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v12 + 40LL))(v12, &v28, 4);
  if ( v12[4] != 0 )
    return 0;
  v15 = (_DWORD *)*a2;
  v16 = a1[6];
  v17 = v16 != 0 ? *(_DWORD *)(v16 + 8) : -1;
  v27 = v17;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v15 + 40LL))(v15, &v27, 4);
  if ( v15[4] != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 7, 4);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 60, 4);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 69, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 70, 1);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 71, 1);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return 0;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 9, 1);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
