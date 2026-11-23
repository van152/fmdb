bool __fastcall sub_14151C2A0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  unsigned int v7; // eax
  _DWORD *v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rbp
  __int64 v11; // r15
  __int64 v12; // rbx
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // r14
  bool v16; // al
  __int64 v17; // r15
  __int64 v18; // rbx
  _DWORD *v19; // rbx
  __int64 v20; // r12
  unsigned __int64 v21; // rax
  unsigned __int64 v22; // r13
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // r13
  __int64 v25; // rbp
  _DWORD *v26; // r14
  __int64 v27; // rbx
  unsigned __int64 v28; // rcx
  __int64 v29; // r8
  __int64 v30; // r14
  bool v31; // al
  __int64 v32; // rbx
  __int64 v33; // rbx
  __int64 v34; // rbx
  __int64 v35; // rbp
  __int64 v36; // rbx
  _DWORD *v37; // rbx
  __int64 v38; // r13
  unsigned __int64 v39; // rax
  unsigned __int64 v40; // r14
  unsigned __int64 v41; // rcx
  unsigned __int64 v42; // r14
  __int64 v43; // r12
  _DWORD *v44; // r15
  __int64 v45; // rbx
  __int64 v46; // rbx
  int v48; // [rsp+20h] [rbp-68h] BYREF
  unsigned int v49; // [rsp+28h] [rbp-60h] BYREF
  char v50; // [rsp+2Fh] [rbp-59h] BYREF
  unsigned __int64 v51; // [rsp+30h] [rbp-58h]
  int v52; // [rsp+3Ch] [rbp-4Ch] BYREF
  _QWORD *v53; // [rsp+40h] [rbp-48h]

  v52 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v52, 4);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v50, 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v49, 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = v49;
  *(_DWORD *)a1 = v49 & 0xFF7FFFFF;
  if ( (v7 & 0x800000) != 0 )
  {
    sub_1408386A0(*a2, &v48, a1 + 8);
    if ( v48 != 0 )
      return false;
  }
  v8 = (_DWORD *)*a2;
  if ( *(_DWORD *)(*a2 + 16LL) != 0 )
    return false;
  v49 = 0;
  (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)v8 + 40LL))(v8, &v49, 4);
  if ( v8[4] != 0 )
    return false;
  v9 = *(_QWORD *)(a1 + 24);
  if ( v9 != *(_QWORD *)(a1 + 32) )
    *(_QWORD *)(a1 + 32) = v9;
  v10 = v49;
  if ( (*(_QWORD *)(a1 + 40) - v9) >> 2 < (unsigned __int64)v49 )
  {
    v11 = sub_1407E4490(qword_141ABD470, 4LL * v49);
    sub_141758A00();
    v12 = *(_QWORD *)(a1 + 24);
    if ( v12 != 0 )
    {
      v13 = *(_QWORD *)(a1 + 40) - v12;
      if ( v13 == -1 )
        v13 = *(unsigned int *)(v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v14 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13)
        && (v15 = *(_QWORD *)(v14 + 8 * v13)) != 0 )
      {
        MEMORY[0x1419475D8](v15 + 32, v12 - *(unsigned int *)(v15 + 120));
        v16 = *(_BYTE *)(v15 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) != 0;
        if ( !v16 && *(_BYTE *)(v15 + 97) != 0 )
          sub_1412D33C0(v15);
      }
      else
      {
        MEMORY[0x141948990](v12 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *(_QWORD *)(a1 + 24) = v11;
    *(_QWORD *)(a1 + 32) = v11;
    *(_QWORD *)(a1 + 40) = v11 + 4 * v10;
    LODWORD(v10) = v49;
  }
  if ( (_DWORD)v10 != 0 )
  {
    v17 = 0;
    do
    {
      v48 = 0;
      v18 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v48, 4);
      if ( *(_DWORD *)(v18 + 16) != 0 )
        return false;
      v19 = *(_DWORD **)(a1 + 32);
      if ( v19 == *(_DWORD **)(a1 + 40) )
      {
        v20 = (__int64)v19 - *(_QWORD *)(a1 + 24);
        v21 = v20 >> 2;
        v22 = (unsigned __int64)(v20 >> 2) >> 1;
        v23 = 0x3FFFFFFFFFFFFFFFLL - v22;
        v24 = (v20 >> 2) + v22;
        v51 = (v20 >> 2) + 1;
        if ( v24 <= v51 )
          v24 = v21 + 1;
        if ( v21 > v23 )
          v24 = 0x3FFFFFFFFFFFFFFFLL;
        v25 = sub_1407E4490(qword_141ABD470, 4 * v24);
        *(_DWORD *)(v25 + v20) = v48;
        v26 = *(_DWORD **)(a1 + 32);
        sub_141758A00();
        if ( v26 != v19 )
          sub_141758A00();
        v27 = *(_QWORD *)(a1 + 24);
        if ( v27 != 0 )
        {
          v28 = *(_QWORD *)(a1 + 40) - v27;
          if ( v28 == -1 )
            v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v29 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28)
            && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
          {
            MEMORY[0x1419475D8](v30 + 32, v27 - *(unsigned int *)(v30 + 120));
            v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
            if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
              sub_1412D33C0(v30);
          }
          else
          {
            MEMORY[0x141948990](v27 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        *(_QWORD *)(a1 + 24) = v25;
        *(_QWORD *)(a1 + 32) = v25 + 4 * v51;
        *(_QWORD *)(a1 + 40) = v25 + 4 * v24;
      }
      else
      {
        *v19 = v48;
        *(_QWORD *)(a1 + 32) += 4LL;
      }
    }
    while ( ++v17 < (unsigned __int64)v49 );
  }
  v32 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 4);
  if ( *(_DWORD *)(v32 + 16) != 0 )
    return false;
  v33 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 2);
  if ( *(_DWORD *)(v33 + 16) != 0 )
    return false;
  v34 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v49, 4);
  if ( *(_DWORD *)(v34 + 16) != 0 )
    return false;
  v53 = (_QWORD *)(a1 + 56);
  sub_141011F70(a1 + 56, v49);
  if ( v49 != 0 )
  {
    v35 = 0;
    do
    {
      v48 = 0;
      v36 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v48, 4);
      if ( *(_DWORD *)(v36 + 16) != 0 )
        return false;
      v37 = *(_DWORD **)(a1 + 64);
      if ( v37 == *(_DWORD **)(a1 + 72) )
      {
        v38 = (__int64)v37 - *(_QWORD *)(a1 + 56);
        v39 = v38 >> 2;
        v40 = (unsigned __int64)(v38 >> 2) >> 1;
        v41 = 0x3FFFFFFFFFFFFFFFLL - v40;
        v42 = (v38 >> 2) + v40;
        v51 = (v38 >> 2) + 1;
        if ( v42 <= v51 )
          v42 = v39 + 1;
        if ( v39 > v41 )
          v42 = 0x3FFFFFFFFFFFFFFFLL;
        v43 = sub_1407E4490(qword_141ABD470, 4 * v42);
        *(_DWORD *)(v43 + v38) = v48;
        v44 = *(_DWORD **)(a1 + 64);
        sub_141758A00();
        if ( v44 != v37 )
          sub_141758A00();
        if ( *v53 != 0 )
          sub_1407E4890(qword_141ABD470, *v53, *(_QWORD *)(a1 + 72) - *v53);
        *(_QWORD *)(a1 + 56) = v43;
        *(_QWORD *)(a1 + 64) = v43 + 4 * v51;
        *(_QWORD *)(a1 + 72) = v43 + 4 * v42;
      }
      else
      {
        *v37 = v48;
        *(_QWORD *)(a1 + 64) += 4LL;
      }
    }
    while ( ++v35 < (unsigned __int64)v49 );
  }
  v45 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 80, 4);
  if ( *(_DWORD *)(v45 + 16) != 0 )
    return false;
  v46 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 1);
  if ( *(_DWORD *)(v46 + 16) != 0 )
    return false;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
