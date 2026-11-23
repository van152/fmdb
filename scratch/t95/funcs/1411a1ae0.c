__int64 __fastcall sub_1411A1AE0(__int64 a1, _QWORD *a2, unsigned int a3, unsigned int a4)
{
  unsigned int v5; // ebx
  _DWORD *v8; // rdi
  _DWORD *v9; // rdi
  __int64 v10; // rdi
  _DWORD *v11; // rdi
  __int64 v12; // rax
  int v13; // eax
  _DWORD *v14; // rdi
  __int64 v15; // rax
  int v16; // eax
  _DWORD *v17; // rdi
  __int64 v18; // rax
  int v19; // eax
  _DWORD *v20; // rdi
  __int64 v21; // rax
  int v22; // eax
  _DWORD *v23; // r14
  __int64 v24; // rax
  int v25; // eax
  _DWORD *v26; // rdi
  __int64 v27; // rax
  int v28; // eax
  __int64 v29; // rdi
  _DWORD *v30; // rdi
  __int64 v31; // rax
  int v32; // eax
  _DWORD *v33; // rdi
  __int64 v34; // rax
  unsigned __int64 v35; // r12
  __int64 v36; // rax
  int v37; // eax
  __int64 v38; // rdi
  _DWORD *v39; // rdi
  __int64 v40; // rax
  int v41; // eax
  _DWORD *v42; // rdi
  __int64 v43; // rax
  int v44; // eax
  __int64 v45; // rdi
  __int64 v46; // rdi
  __int64 v47; // rdi
  __int64 v48; // rdi
  __int64 v49; // rdi
  _DWORD *v50; // rdi
  __int64 v51; // rax
  int v52; // eax
  __int64 v53; // rdi
  _DWORD v55[15]; // [rsp+2Ch] [rbp-3Ch] BYREF

  v5 = a3;
  if ( (_BYTE)a3 != 0 )
  {
    v8 = (_DWORD *)*a2;
    LOBYTE(v55[0]) = 10;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v55, 1);
    if ( v8[4] != 0 )
      return 0;
  }
  if ( (_BYTE)a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 176, 1);
    if ( v9[4] != 0 )
      return 0;
    v10 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 171, 1);
    if ( *(_DWORD *)(v10 + 16) != 0 )
      return 0;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 168, 2);
    v11 = (_DWORD *)*a2;
    v12 = *(_QWORD *)(a1 + 80);
    v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
    v55[0] = v13;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, v55, 4);
    if ( v11[4] != 0 )
      return 0;
    v14 = (_DWORD *)*a2;
    v15 = *(_QWORD *)(a1 + 96);
    v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
    v55[0] = v16;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v14 + 40LL))(v14, v55, 4);
    if ( v14[4] != 0 )
      return 0;
    v17 = (_DWORD *)*a2;
    v18 = *(_QWORD *)(a1 + 88);
    v19 = v18 != 0 ? *(_DWORD *)(v18 + 8) : -1;
    v55[0] = v19;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, v55, 4);
    if ( v17[4] != 0 )
      return 0;
    v20 = (_DWORD *)*a2;
    v21 = *(_QWORD *)(a1 + 120);
    v22 = v21 != 0 ? *(_DWORD *)(v21 + 8) : -1;
    v55[0] = v22;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v20 + 40LL))(v20, v55, 4);
    if ( v20[4] != 0 )
      return 0;
    v23 = (_DWORD *)*a2;
    v24 = *(_QWORD *)(a1 + 128);
    v25 = v24 != 0 ? *(_DWORD *)(*(int *)(*(_QWORD *)(v24 + 8) + 4LL) + v24 + 16) : -1;
    v55[0] = v25;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v23 + 40LL))(v23, v55, 4);
    if ( v23[4] != 0 )
      return 0;
    v26 = (_DWORD *)*a2;
    v27 = *(_QWORD *)(a1 + 152);
    v28 = v27 != 0 ? *(_DWORD *)(v27 + 8) : -1;
    v55[0] = v28;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v26 + 40LL))(v26, v55, 4);
    if ( v26[4] != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 175, 1);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return 0;
    v30 = (_DWORD *)*a2;
    v31 = *(_QWORD *)(a1 + 104);
    v32 = v31 != 0 ? *(_DWORD *)(v31 + 8) : -1;
    v55[0] = v32;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v30 + 40LL))(v30, v55, 4);
    if ( v30[4] != 0 )
      return 0;
    v33 = (_DWORD *)*a2;
    LOWORD(v55[0]) = (unsigned int)(*(_DWORD *)(a1 + 64) - *(_DWORD *)(a1 + 56)) >> 3;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v33 + 40LL))(v33, v55, 2);
    if ( v33[4] != 0 )
      return 0;
    v34 = *(_QWORD *)(a1 + 56);
    if ( *(_QWORD *)(a1 + 64) != v34 )
    {
      v35 = 0;
      do
      {
        v36 = *(_QWORD *)(v34 + 8 * v35);
        v37 = v36 != 0 ? *(_DWORD *)(*(int *)(*(_QWORD *)(v36 + 8) + 4LL) + v36 + 16) : -1;
        v55[0] = v37;
        v38 = *a2;
        (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v55, 4);
        if ( *(_DWORD *)(v38 + 16) != 0 )
          return 0;
        ++v35;
        v34 = *(_QWORD *)(a1 + 56);
      }
      while ( v35 < (*(_QWORD *)(a1 + 64) - v34) >> 3 );
    }
    v39 = (_DWORD *)*a2;
    v40 = *(_QWORD *)(a1 + 136);
    v41 = v40 != 0 ? *(_DWORD *)(v40 + 8) : -1;
    v55[0] = v41;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v39 + 40LL))(v39, v55, 4);
    if ( v39[4] != 0 )
      return 0;
    v42 = (_DWORD *)*a2;
    v43 = *(_QWORD *)(a1 + 144);
    v44 = v43 != 0 ? *(_DWORD *)(v43 + 8) : -1;
    v55[0] = v44;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v42 + 40LL))(v42, v55, 4);
    if ( v42[4] != 0 )
      return 0;
    v45 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 170, 1);
    if ( *(_DWORD *)(v45 + 16) != 0 )
      return 0;
    v46 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 172, 1);
    if ( *(_DWORD *)(v46 + 16) != 0 )
      return 0;
    v47 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 173, 1);
    if ( *(_DWORD *)(v47 + 16) != 0 )
      return 0;
    v48 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 174, 1);
    if ( *(_DWORD *)(v48 + 16) != 0 )
      return 0;
    v49 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 177, 1);
    if ( *(_DWORD *)(v49 + 16) != 0 )
      return 0;
    v50 = (_DWORD *)*a2;
    v51 = *(_QWORD *)(a1 + 112);
    v52 = v51 != 0 ? *(_DWORD *)(v51 + 8) : -1;
    v55[0] = v52;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v50 + 40LL))(v50, v55, 4);
    if ( v50[4] != 0 )
      return 0;
    v53 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 178, 1);
    if ( *(_DWORD *)(v53 + 16) != 0 )
      return 0;
  }
  if ( (_BYTE)v5 == 0 || (v5 = 0, (unsigned __int8)sub_1411C2990(a1, a2, 0, a4) != 0) )
    LOBYTE(v5) = 1;
  return v5;
}
