bool __fastcall sub_14451B780(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  int *v5; // rdx
  __int64 v6; // rax
  __int64 v7; // rax
  int v8; // eax
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbx
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rbx
  __int64 v24; // rbx
  __int64 v25; // rbx
  _DWORD *v27; // rdi
  int v28; // [rsp+24h] [rbp-24h] BYREF
  int v29; // [rsp+28h] [rbp-20h] BYREF
  int v30; // [rsp+2Ch] [rbp-1Ch] BYREF

  v4 = (_DWORD *)*a2;
  if ( *(int *)(a1 + 80) < 0 )
  {
    v7 = *(_QWORD *)(a1 + 24);
    if ( v7 != 0 )
      v8 = *(_DWORD *)(v7 + 8);
    else
      v8 = -1;
    v30 = v8;
    v6 = *(_QWORD *)v4;
    v5 = &v30;
  }
  else
  {
    v5 = (int *)(a1 + 80);
    v6 = *(_QWORD *)v4;
  }
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(v6 + 40))(v4, v5, 4);
  if ( v4[4] != 0 )
    return false;
  v9 = (_DWORD *)*a2;
  v10 = *(_QWORD *)(a1 + 40);
  v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
  v29 = v11;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v9 + 40LL))(v9, &v29, 4);
  if ( v9[4] != 0 )
    return false;
  v12 = (_DWORD *)*a2;
  v13 = *(_QWORD *)(a1 + 32);
  v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
  v28 = v14;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v12 + 40LL))(v12, &v28, 4);
  if ( v12[4] != 0 )
    return false;
  v15 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 2);
  if ( v15[4] != 0 )
    return false;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 50, 2);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return false;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 2);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return false;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 54, 2);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_14156AAB0(a1 + 56, a2) == 0 )
    return false;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 72, 8);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return false;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 102, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return false;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 88, 4);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return false;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 92, 4);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return false;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 100, 2);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return false;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 4);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return false;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 103, 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return false;
  v27 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v27 + 40LL))(v27, a1 + 96, 4);
  return v27[4] == 0;
}
