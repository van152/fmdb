bool __fastcall sub_1411D3570(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rdi
  _DWORD *v8; // rdi
  __int64 v9; // rdi
  _DWORD *v11; // rdi
  __int64 v12; // rax
  unsigned __int64 v13; // rbx
  _DWORD *v14; // rdi
  _DWORD *v15; // rdi
  __int64 v16; // rax
  unsigned __int64 v17; // rbx
  _DWORD *v18; // rdi
  char v19; // cl
  __int64 v20; // rdi
  __int64 v21; // rbx
  _DWORD *v22; // rdi
  __int64 v23; // rax
  char v24; // cl
  __int64 v25; // rdi
  __int64 v26; // rbx
  _DWORD *v27; // rdi
  __int64 v28; // rax
  char v29; // cl
  __int64 v30; // rdi
  __int64 v31; // rbx
  _DWORD *v32; // rdi
  __int64 v33; // rax
  __int64 v34; // rcx
  __int64 v35; // rdi
  __int64 v36; // rax
  __int64 v37; // rdi
  unsigned __int64 i; // rbx
  _DWORD *v39; // rcx
  unsigned int v40; // eax
  __int64 v41; // rdi
  __int64 v42; // rdi
  __int64 v43; // rdi
  __int64 v44; // rdi
  __int64 v45; // rdi
  __int64 v46; // rdx
  unsigned __int8 v47; // [rsp+24h] [rbp-54h] BYREF
  char v48; // [rsp+25h] [rbp-53h] BYREF
  char v49; // [rsp+26h] [rbp-52h] BYREF
  char v50; // [rsp+27h] [rbp-51h] BYREF
  __int64 v51; // [rsp+28h] [rbp-50h] BYREF
  __int64 v52; // [rsp+30h] [rbp-48h]
  __int64 v53; // [rsp+38h] [rbp-40h]
  __int64 v54; // [rsp+40h] [rbp-38h]

  v7 = (_DWORD *)*a2;
  LOBYTE(v51) = *(_BYTE *)(a1 + 186);
  (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v51, 1);
  if ( v7[4] != 0 )
    return false;
  v8 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 184, 1);
  if ( v8[4] != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 185, 1);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  if ( a4 != 0 )
  {
    v11 = (_DWORD *)*a2;
    LOBYTE(v51) = (unsigned int)(*(_DWORD *)(a1 + 32) - *(_DWORD *)(a1 + 24)) >> 3;
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v11 + 40LL))(v11, &v51, 1);
    if ( v11[4] != 0 )
      return false;
    v12 = *(_QWORD *)(a1 + 24);
    if ( *(_QWORD *)(a1 + 32) != v12 )
    {
      v13 = 0;
      do
      {
        v14 = (_DWORD *)*a2;
        LODWORD(v51) = *(_DWORD *)(*(_QWORD *)(v12 + 8 * v13) + 8LL);
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v14 + 40LL))(v14, &v51, 4);
        if ( v14[4] != 0 )
          return false;
        ++v13;
        v12 = *(_QWORD *)(a1 + 24);
      }
      while ( v13 < (*(_QWORD *)(a1 + 32) - v12) >> 3 );
    }
    v15 = (_DWORD *)*a2;
    LOBYTE(v51) = (unsigned int)(*(_DWORD *)(a1 + 56) - *(_DWORD *)(a1 + 48)) >> 3;
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v15 + 40LL))(v15, &v51, 1);
    if ( v15[4] != 0 )
      return false;
    v16 = *(_QWORD *)(a1 + 48);
    if ( *(_QWORD *)(a1 + 56) != v16 )
    {
      v17 = 0;
      do
      {
        v18 = (_DWORD *)*a2;
        LODWORD(v51) = *(_DWORD *)(*(_QWORD *)(v16 + 8 * v17) + 8LL);
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v18 + 40LL))(v18, &v51, 4);
        if ( v18[4] != 0 )
          return false;
        ++v17;
        v16 = *(_QWORD *)(a1 + 48);
      }
      while ( v17 < (*(_QWORD *)(a1 + 56) - v16) >> 3 );
    }
    v19 = 100;
    if ( (char)((unsigned int)(*(_DWORD *)(a1 + 104) - *(_DWORD *)(a1 + 96)) >> 3) < 100 )
      v19 = (unsigned int)(*(_DWORD *)(a1 + 104) - *(_DWORD *)(a1 + 96)) >> 3;
    v50 = v19;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v50, 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return false;
    if ( v50 > 0 )
    {
      v21 = 0;
      do
      {
        v22 = (_DWORD *)*a2;
        v23 = *(_QWORD *)(*(_QWORD *)(a1 + 96) + 8 * v21);
        LODWORD(v51) = *(_DWORD *)(*(int *)(*(_QWORD *)(v23 + 8) + 4LL) + v23 + 16);
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v22 + 40LL))(v22, &v51, 4);
        if ( v22[4] != 0 )
          return false;
      }
      while ( ++v21 < v50 );
    }
    v24 = 100;
    if ( (char)((unsigned int)(*(_DWORD *)(a1 + 128) - *(_DWORD *)(a1 + 120)) >> 3) < 100 )
      v24 = (unsigned int)(*(_DWORD *)(a1 + 128) - *(_DWORD *)(a1 + 120)) >> 3;
    v49 = v24;
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v49, 1);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return false;
    if ( v49 > 0 )
    {
      v26 = 0;
      do
      {
        v27 = (_DWORD *)*a2;
        v28 = *(_QWORD *)(*(_QWORD *)(a1 + 120) + 8 * v26);
        LODWORD(v51) = *(_DWORD *)(*(int *)(*(_QWORD *)(v28 + 8) + 4LL) + v28 + 16);
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v27 + 40LL))(v27, &v51, 4);
        if ( v27[4] != 0 )
          return false;
      }
      while ( ++v26 < v49 );
    }
    v29 = 100;
    if ( (char)((unsigned int)(*(_DWORD *)(a1 + 152) - *(_DWORD *)(a1 + 144)) >> 3) < 100 )
      v29 = (unsigned int)(*(_DWORD *)(a1 + 152) - *(_DWORD *)(a1 + 144)) >> 3;
    v48 = v29;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v48, 1);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return false;
    if ( v48 > 0 )
    {
      v31 = 0;
      do
      {
        v32 = (_DWORD *)*a2;
        v33 = *(_QWORD *)(*(_QWORD *)(a1 + 144) + 8 * v31);
        LODWORD(v51) = *(_DWORD *)(*(int *)(*(_QWORD *)(v33 + 8) + 4LL) + v33 + 16);
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v32 + 40LL))(v32, &v51, 4);
        if ( v32[4] != 0 )
          return false;
      }
      while ( ++v31 < v48 );
    }
    LOBYTE(v34) = -1;
    if ( (unsigned __int64)((__int64)(*(_QWORD *)(a1 + 80) - *(_QWORD *)(a1 + 72)) >> 4) < 0xFF )
      v34 = (__int64)(*(_QWORD *)(a1 + 80) - *(_QWORD *)(a1 + 72)) >> 4;
    v47 = v34;
    v35 = *a2;
    (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v47, 1);
    if ( *(_DWORD *)(v35 + 16) != 0 )
      return false;
    v36 = *a2;
    v51 = v36;
    if ( v36 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v36 + 8));
    v54 = 0;
    v53 = 0;
    v52 = 0;
    if ( v47 != 0 )
    {
      v37 = 0;
      for ( i = 0; i < v47; ++i )
      {
        sub_1411066E0(v37 + *(_QWORD *)(a1 + 72), &v51);
        v37 += 16;
      }
      if ( v53 != 0 && v51 != 0 )
        (*(void (__fastcall **)(__int64, __int64))(*(_QWORD *)v51 + 40LL))(v51, v52);
    }
    v54 = 0;
    v53 = 0;
    v52 = 0;
    sub_1412E6FF0(&v51);
    v39 = *(_DWORD **)(a1 + 168);
    if ( v39 != nullptr )
      v40 = (unsigned int)(v39[2] - *v39) >> 3;
    else
      LOWORD(v40) = 0;
    LOWORD(v51) = v40;
    v41 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v51, 2);
    if ( *(_DWORD *)(v41 + 16) != 0 )
      return false;
    if ( (_WORD)v51 != 0 )
    {
      v42 = 0;
      while ( (unsigned __int8)sub_1411D3A90(*(_QWORD *)(**(_QWORD **)(a1 + 168) + 8 * v42), a2) != 0 )
      {
        if ( ++v42 >= (unsigned __int64)(unsigned __int16)v51 )
          goto LABEL_56;
      }
      return false;
    }
  }
LABEL_56:
  v43 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v43 + 16) != 0 )
    return false;
  v44 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v44 + 16) != 0 )
    return false;
  v45 = *a2;
  v46 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v46, 4);
  return *(_DWORD *)(v45 + 16) == 0;
}
