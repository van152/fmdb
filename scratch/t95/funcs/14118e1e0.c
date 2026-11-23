bool __fastcall sub_14118E1E0(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rsi
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rsi
  _DWORD *v13; // rbx
  __int64 v14; // rax
  int v15; // eax
  _DWORD *v16; // rbx
  __int64 v17; // rax
  int v18; // eax
  _DWORD *v19; // rbx
  __int64 v20; // rax
  int v21; // eax
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  _DWORD *v31; // rbx
  __int64 v32; // rax
  int v33; // eax
  _DWORD *v34; // rbx
  __int64 v35; // rax
  int v36; // eax
  _DWORD *v37; // rbx
  __int64 v38; // rax
  int v39; // eax
  __int64 v40; // rsi
  __int64 v41; // rsi
  __int64 v42; // rsi
  __int64 v43; // rsi
  __int64 v44; // rsi
  __int64 v45; // rsi
  __int64 v46; // rsi
  _DWORD *v47; // rdi
  __int64 v48; // rdx
  _DWORD v49[10]; // [rsp+20h] [rbp-28h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v49[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v49, 1);
  if ( v7[4] != 0 )
    return false;
  if ( a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 24);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    v49[0] = v11;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v49, 4);
    if ( v9[4] != 0 )
      return false;
    v12 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 140, 2);
    if ( v12[4] != 0 )
      return false;
    v13 = (_DWORD *)*a2;
    v14 = *(_QWORD *)(a1 + 32);
    v15 = v14 != 0 ? *(_DWORD *)(v14 + 8) : -1;
    v49[0] = v15;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v13 + 40LL))(v13, v49, 4);
    if ( v13[4] != 0 )
      return false;
    v16 = (_DWORD *)*a2;
    v17 = *(_QWORD *)(a1 + 48);
    v18 = v17 != 0 ? *(_DWORD *)(v17 + 8) : -1;
    v49[0] = v18;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v16 + 40LL))(v16, v49, 4);
    if ( v16[4] != 0 )
      return false;
    v19 = (_DWORD *)*a2;
    v20 = *(_QWORD *)(a1 + 72);
    v21 = v20 != 0 ? *(_DWORD *)(v20 + 8) : -1;
    v49[0] = v21;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v19 + 40LL))(v19, v49, 4);
    if ( v19[4] != 0 )
      return false;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 142, 2);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      return false;
    v23 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 146, 2);
    if ( *(_DWORD *)(v23 + 16) != 0 )
      return false;
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 150, 2);
    if ( *(_DWORD *)(v24 + 16) != 0 )
      return false;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 144, 2);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return false;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 148, 2);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return false;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 152, 2);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return false;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 128, 4);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return false;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 132, 4);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return false;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 136, 4);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return false;
    sub_1408149D0(*a2, v49, a1 + 80);
    if ( v49[0] != 0 )
      return false;
    sub_1408149D0(*a2, v49, a1 + 88);
    if ( v49[0] != 0 )
      return false;
    sub_1408149D0(*a2, v49, a1 + 96);
    if ( v49[0] != 0
      || (unsigned __int8)sub_140FEA120(a1 + 104, a2) == 0
      || (unsigned __int8)sub_140FEA120(a1 + 112, a2) == 0
      || (unsigned __int8)sub_140FEA120(a1 + 120, a2) == 0 )
    {
      return false;
    }
    v31 = (_DWORD *)*a2;
    v32 = *(_QWORD *)(a1 + 40);
    v33 = v32 != 0 ? *(_DWORD *)(v32 + 8) : -1;
    v49[0] = v33;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v31 + 40LL))(v31, v49, 4);
    if ( v31[4] != 0 )
      return false;
    v34 = (_DWORD *)*a2;
    v35 = *(_QWORD *)(a1 + 56);
    v36 = v35 != 0 ? *(_DWORD *)(v35 + 8) : -1;
    v49[0] = v36;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v34 + 40LL))(v34, v49, 4);
    if ( v34[4] != 0 )
      return false;
    v37 = (_DWORD *)*a2;
    v38 = *(_QWORD *)(a1 + 64);
    v39 = v38 != 0 ? *(_DWORD *)(v38 + 8) : -1;
    v49[0] = v39;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v37 + 40LL))(v37, v49, 4);
    if ( v37[4] != 0 )
      return false;
    v40 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 155, 1);
    if ( *(_DWORD *)(v40 + 16) != 0 )
      return false;
    v41 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 156, 1);
    if ( *(_DWORD *)(v41 + 16) != 0 )
      return false;
    v42 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 154, 1);
    if ( *(_DWORD *)(v42 + 16) != 0 )
      return false;
    v43 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 157, 1);
    if ( *(_DWORD *)(v43 + 16) != 0 )
      return false;
    v44 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 158, 1);
    if ( *(_DWORD *)(v44 + 16) != 0 )
      return false;
  }
  v45 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v45 + 16) != 0 )
    return false;
  v46 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v46 + 16) != 0 )
    return false;
  v47 = (_DWORD *)*a2;
  v48 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v47 + 40LL))(v47, v48, 4);
  return v47[4] == 0;
}
