bool __fastcall sub_141192180(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  __int64 v5; // rax
  int v6; // eax
  _DWORD *v7; // rbx
  __int64 v8; // rax
  int v9; // eax
  _DWORD *v10; // rbx
  __int64 v11; // rax
  int v12; // eax
  _DWORD *v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  _QWORD *v21; // rbx
  _QWORD *v22; // r14
  __int64 v23; // rbx
  __int64 v24; // rbx
  __int64 v25; // rbx
  __int64 v26; // rbx
  _DWORD *v27; // rbx
  __int64 v29; // rbx
  __int64 v30; // r14
  _DWORD *v31; // rdi
  char v32; // [rsp+29h] [rbp-2Fh] BYREF
  __int16 v33; // [rsp+2Ah] [rbp-2Eh] BYREF
  int v34; // [rsp+2Ch] [rbp-2Ch] BYREF
  int v35; // [rsp+30h] [rbp-28h] BYREF
  int v36[9]; // [rsp+34h] [rbp-24h] BYREF

  v4 = (_DWORD *)*a2;
  v5 = *(_QWORD *)(a1 + 72);
  if ( v5 != 0 )
    v6 = *(_DWORD *)(v5 + 8);
  else
    v6 = -1;
  v36[0] = v6;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v4 + 40LL))(v4, v36, 4);
  if ( v4[4] != 0 )
    return false;
  v7 = (_DWORD *)*a2;
  v8 = *(_QWORD *)(a1 + 80);
  v9 = v8 != 0 ? *(_DWORD *)(v8 + 8) : -1;
  v35 = v9;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v35, 4);
  if ( v7[4] != 0 )
    return false;
  v10 = (_DWORD *)*a2;
  v11 = *(_QWORD *)(a1 + 88);
  v12 = v11 != 0 ? *(_DWORD *)(v11 + 8) : -1;
  v34 = v12;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v10 + 40LL))(v10, &v34, 4);
  if ( v10[4] != 0 )
    return false;
  v13 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 104, 2);
  if ( v13[4] != 0 )
    return false;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 106, 2);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return false;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 108, 4);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return false;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 112, 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return false;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 126, 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140DB89D0() == 0 )
    return false;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 127, 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return false;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 124, 2);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return false;
  v33 = (unsigned int)(*(_DWORD *)(a1 + 32) - *(_DWORD *)(a1 + 24)) >> 3;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v33, 2);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return false;
  v21 = *(_QWORD **)(a1 + 24);
  v22 = *(_QWORD **)(a1 + 32);
  if ( v21 != v22 )
  {
    while ( (unsigned __int8)sub_141192480(*v21, a2) != 0 )
    {
      if ( ++v21 == v22 )
        goto LABEL_25;
    }
    return false;
  }
LABEL_25:
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 128, 1);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return false;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 129, 1);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return false;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 130, 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return false;
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 96, 8);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    return false;
  v27 = (_DWORD *)*a2;
  v32 = (unsigned int)(*(_DWORD *)(a1 + 56) - *(_DWORD *)(a1 + 48)) >> 5;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v27 + 40LL))(v27, &v32, 1);
  if ( v27[4] != 0 )
    return false;
  v29 = *(_QWORD *)(a1 + 48);
  v30 = *(_QWORD *)(a1 + 56);
  if ( v29 != v30 )
  {
    while ( (unsigned __int8)sub_14156AC20(v29, a2) != 0 )
    {
      v29 += 32;
      if ( v29 == v30 )
        goto LABEL_34;
    }
    return false;
  }
LABEL_34:
  v31 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v31 + 40LL))(v31, a1 + 131, 1);
  return v31[4] == 0;
}
