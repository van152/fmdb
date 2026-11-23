__int64 __fastcall sub_140B4B460(_QWORD *a1, int a2)
{
  volatile signed __int32 *v4; // rdi
  __int64 v5; // rdi
  __int64 v6; // rbx
  __int64 v7; // r8
  volatile signed __int32 *v8; // rcx
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // rdi
  volatile signed __int32 *v11; // rdi
  volatile signed __int32 *v12; // rdi
  volatile signed __int32 *v13; // rcx
  int v15; // eax
  __int64 v16; // rbx
  __int64 v17; // r14
  __int64 v18; // rbp
  __int64 v19; // rdi
  __int64 v20; // rdx
  int v21; // r15d
  __int64 v22; // rbx
  char v23; // bp
  volatile signed __int32 *v24; // rcx
  __int64 *v25; // rdi
  unsigned __int64 v26; // rbp
  unsigned __int64 v27; // r13
  unsigned __int64 v28; // rsi
  __int64 v29; // rcx
  __int64 v30; // rcx
  __int64 v31; // r12
  char *v32; // rax
  char *v33; // r14
  __int64 *v34; // rbx
  __int64 v35; // rdx
  char v36; // bl
  volatile signed __int32 *v37; // rcx
  volatile signed __int32 *v38; // rdi
  int v39; // r13d
  __int64 v40; // rbp
  char v41; // bl
  volatile signed __int32 *v42; // rcx
  __int64 *v43; // r14
  __int64 *v44; // rdi
  __int64 v45; // r12
  unsigned __int64 v46; // rax
  unsigned __int64 v47; // r15
  unsigned __int64 v48; // rcx
  unsigned __int64 v49; // r15
  __int64 v50; // rbx
  __int64 *v51; // rbp
  __int64 v52; // rsi
  __int64 v53; // r8
  volatile signed __int32 *v54; // rcx
  __int64 v55; // rcx
  char v56; // bl
  volatile signed __int32 *v57; // rcx
  __int64 v58; // rsi
  __int64 v59; // r8
  volatile signed __int32 *v60; // [rsp+40h] [rbp-78h] BYREF
  volatile signed __int32 *v61; // [rsp+48h] [rbp-70h] BYREF
  volatile signed __int32 *v62; // [rsp+50h] [rbp-68h] BYREF
  unsigned int v63; // [rsp+58h] [rbp-60h] BYREF
  int v64; // [rsp+5Ch] [rbp-5Ch] BYREF
  _QWORD *v65; // [rsp+60h] [rbp-58h]
  unsigned __int64 v66; // [rsp+68h] [rbp-50h]
  __int64 v67; // [rsp+70h] [rbp-48h] BYREF

  v67 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: &v60, a2: 0x1418E2C24LL);
  sub_1407D0F70(
    a1: (unsigned int)&v67,
    a2: (unsigned int)&v62,
    a3: a2,
    a4: (unsigned int)&qword_141B5B7B0,
    a5: (__int64)&v60,
    a6: 0,
    a7: 0,
    0);
  v4 = v62;
  if ( v62 == nullptr )
  {
    LOBYTE(a1) = 1;
    return (unsigned int)a1;
  }
  if ( dword_141B5B7D0 != 0 )
  {
    v5 = qword_141B5AD60;
    v60 = nullptr;
    v6 = sub_1412EC810(a1: 264, a2: 32);
    *(_QWORD *)v6 = 0x2000000000LL;
    strcpy((char *)(v6 + 8), "fixture groups count already set");
    if ( v60 != nullptr )
    {
      v8 = v60 - 1;
      if ( _InterlockedDecrement(v60 - 1) == 0 )
        sub_1412EC9A0(a1: v8);
    }
    v60 = nullptr;
    _InterlockedIncrement((volatile signed __int32 *)v6);
    v60 = (volatile signed __int32 *)(v6 + 4);
    LOBYTE(v7) = 1;
    (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64, _QWORD))(*(_QWORD *)v5 + 120LL))(
      a1: v5,
      a2: &v60,
      a3: v7,
      a4: 0);
    v9 = v60;
    if ( v60 != nullptr && _InterlockedDecrement(v60 - 1) == 0 )
      sub_1412EC9A0(a1: v9 - 1);
    v4 = v62;
  }
  dword_141B5B7D0 = -1431655765 * ((unsigned __int64)(qword_141B5B7C0 - qword_141B5B7B8) >> 3);
  (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v4 + 40LL))(
    a1: v4,
    a2: &dword_141AAB3AC,
    a3: 4);
  if ( *((_DWORD *)v4 + 4) != 0 )
    goto LABEL_14;
  v10 = v62;
  (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v62 + 40LL))(
    a1: v62,
    a2: &dword_141AAB390,
    a3: 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_14;
  v11 = v62;
  (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)v62 + 40LL))(
    a1: v62,
    a2: &word_141B5B8E0,
    a3: 2);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_14;
  v12 = v62;
  (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v62 + 40LL))(a1: v62, a2: &v64, a3: 4);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_14;
  v15 = v64;
  v16 = v64;
  v17 = a1[5];
  if ( (a1[7] - v17) >> 3 < (unsigned __int64)v64 )
  {
    if ( v64 < 0 )
      sub_1400526C0();
    v18 = a1[6];
    v19 = sub_1407E6360(a1: qword_141ABE200, a2: 8LL * v64);
    sub_141758A00(a1: v19, a2: a1[5], a3: a1[6] - a1[5]);
    v20 = a1[5];
    if ( v20 != 0 )
      sub_1407E6420(a1: qword_141ABE200, a2: v20, a3: a1[7] - v20);
    a1[5] = v19;
    a1[6] = v19 + v18 - v17;
    a1[7] = v19 + 8 * v16;
    v15 = v64;
  }
  if ( v15 > 0 )
  {
    v21 = 0;
    v65 = a1;
    while ( 1 )
    {
      if ( dword_141ABDF88 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141ABDF88);
        if ( dword_141ABDF88 == -1 )
        {
          sub_1407E53D0(
            a1: (unsigned int)&unk_141ABDF38,
            a2: 1100152122,
            a3: 512,
            a4: 88,
            a5: 0,
            a6: 0,
            a7: 512,
            a8: 4096);
          sub_141751048(a1: sub_1400525D0);
          sub_141750EA0(a1: &dword_141ABDF88);
        }
      }
      v22 = sub_1407E58C0(a1: &unk_141ABDF38, a2: 88);
      *(_QWORD *)(v22 + 8) = 0;
      *(_QWORD *)(v22 + 16) = 0;
      *(_QWORD *)(v22 + 32) = 0;
      *(_QWORD *)(v22 + 40) = 0;
      *(_DWORD *)(v22 + 64) = 0xFFFF;
      *(_WORD *)(v22 + 69) = -1;
      *(_WORD *)(v22 + 48) = 0;
      *(_QWORD *)(v22 + 24) = 0;
      *(_BYTE *)(v22 + 58) = -1;
      *(_QWORD *)(v22 + 50) = 0xFFFF0000FFFF0000uLL;
      *(_DWORD *)(v22 + 59) = 0x10000;
      *(_BYTE *)(v22 + 63) = 0;
      *(_BYTE *)(v22 + 68) = 2;
      *(_QWORD *)v22 = 0x14186AB38LL;
      *(_QWORD *)(v22 + 72) = 0x76C0001076C0001LL;
      *(_DWORD *)(v22 + 80) = -1;
      *(_BYTE *)(v22 + 84) = -1;
      v60 = v62;
      if ( v62 != nullptr )
        _InterlockedIncrement(v62 + 2);
      v23 = (*(__int64 (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v22 + 264LL))(a1: v22, a2: &v60);
      v24 = v60;
      if ( v60 != nullptr && _InterlockedDecrement(v60 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v24)(a1: v24, a2: 1);
      if ( v23 == 0 )
        break;
      v25 = (__int64 *)a1[6];
      if ( v25 == (__int64 *)a1[7] )
      {
        v26 = ((__int64)v25 - a1[5]) >> 3;
        v27 = v26 + (v26 >> 1);
        v66 = v26 + 1;
        if ( v27 <= v26 + 1 )
          v27 = v26 + 1;
        if ( v26 > 0x1FFFFFFFFFFFFFFFLL - (v26 >> 1) )
          v27 = 0x1FFFFFFFFFFFFFFFLL;
        v28 = 8 * v27;
        if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
          && (v29 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v29) >> 3 > v28)
          && (v30 = *(_QWORD *)(v29 + (v27 << 6))) != 0 )
        {
          v31 = *(unsigned int *)(v30 + 88);
          v32 = (char *)sub_1407E58C0(a1: v30, a2: *(unsigned int *)(v30 + 80));
        }
        else
        {
          v31 = *(unsigned int *)(qword_141ABE200 + 48);
          v32 = (char *)sub_141601260(a1: (unsigned int)(v31 + v28), a2: 4096);
        }
        v33 = v32;
        if ( v31 != 0 )
        {
          *(_DWORD *)v32 = v28;
          v33 = &v32[v31];
        }
        a1 = v65;
        *(_QWORD *)&v33[8 * v26] = v22;
        v34 = (__int64 *)a1[6];
        sub_141758A00(a1: v33, a2: a1[5], a3: (char *)v25 - a1[5]);
        if ( v34 != v25 )
          sub_141758A00(a1: &v33[8 * v26 + 8], a2: v25, a3: a1[6] - (_QWORD)v25);
        v35 = a1[5];
        if ( v35 != 0 )
          sub_1407E6420(a1: qword_141ABE200, a2: v35, a3: a1[7] - v35);
        a1[5] = v33;
        a1[6] = &v33[8 * v66];
        a1[7] = &v33[8 * v27];
      }
      else
      {
        *v25 = v22;
        a1[6] += 8LL;
      }
      if ( ++v21 >= v64 )
        goto LABEL_55;
    }
    v52 = qword_141B5AD60;
    v60 = nullptr;
    sub_140809040(a1: &v60, a2: 0x141903BD0LL, a3: 0xFFFFFFFFLL);
    LOBYTE(v53) = 1;
    (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64, _QWORD))(*(_QWORD *)v52 + 120LL))(
      a1: v52,
      a2: &v60,
      a3: v53,
      a4: 0);
    v54 = v60;
    if ( v60 == nullptr )
      goto LABEL_14;
LABEL_89:
    if ( _InterlockedDecrement(v54 - 1) == 0 )
      sub_1412EC9A0(a1: v54 - 1);
    goto LABEL_14;
  }
LABEL_55:
  v61 = v62;
  if ( v62 != nullptr )
    _InterlockedIncrement(v62 + 2);
  v36 = sub_140B4BD70(a1, a2: &v61, a3: &v60);
  v37 = v61;
  if ( v61 != nullptr && _InterlockedDecrement(v61 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v37)(a1: v37, a2: 1);
  if ( v36 == 0 )
    goto LABEL_14;
  v63 = 0;
  v38 = v62;
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v62 + 40LL))(
    a1: v62,
    a2: &v63,
    a3: 4);
  if ( *((_DWORD *)v38 + 4) != 0 )
    goto LABEL_14;
  if ( v63 != 0 )
  {
    v39 = 0;
    while ( 1 )
    {
      v40 = sub_141750CC0(a1: 72);
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      *(_QWORD *)(v40 + 32) = 0;
      *(_QWORD *)(v40 + 24) = 0;
      *(_QWORD *)(v40 + 16) = 0;
      if ( qword_141ABE200 == 0 )
        qword_141ABE200 = sub_1407E6540();
      *(_QWORD *)(v40 + 8) = 0;
      *(_QWORD *)v40 = 0;
      *(_QWORD *)(v40 + 40) = 0;
      *(_QWORD *)(v40 + 48) = 0;
      *(_QWORD *)(v40 + 56) = 0;
      *(_DWORD *)(v40 + 64) = 0;
      v61 = v62;
      if ( v62 != nullptr )
        _InterlockedIncrement(v62 + 2);
      v41 = sub_140B4BD70(a1: v40, a2: &v61, a3: &v60);
      v42 = v61;
      if ( v61 != nullptr && _InterlockedDecrement(v61 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v42)(a1: v42, a2: 1);
      if ( v41 == 0 )
        break;
      if ( v60 != nullptr )
      {
        v43 = (__int64 *)*a1;
        v44 = *(__int64 **)(*a1 + 8LL);
        if ( v44 == *(__int64 **)(*a1 + 16LL) )
        {
          v45 = (__int64)v44 - *v43;
          v46 = v45 >> 3;
          v47 = (unsigned __int64)(v45 >> 3) >> 1;
          v48 = 0x1FFFFFFFFFFFFFFFLL - v47;
          v49 = (v45 >> 3) + v47;
          v66 = (v45 >> 3) + 1;
          if ( v49 <= v66 )
            v49 = v46 + 1;
          if ( v46 > v48 )
            v49 = 0x1FFFFFFFFFFFFFFFLL;
          v50 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v49);
          *(_QWORD *)(v50 + v45) = v40;
          v51 = (__int64 *)v43[1];
          sub_141758A00(a1: v50, a2: *v43, a3: (char *)v44 - *v43);
          if ( v51 != v44 )
            sub_141758A00(a1: v50 + v45 + 8, a2: v44, a3: v43[1] - (_QWORD)v44);
          if ( *v43 != 0 )
            sub_1407E4890(a1: qword_141ABD470);
          *v43 = v50;
          v43[1] = v50 + 8 * v66;
          v43[2] = v50 + 8 * v49;
        }
        else
        {
          *v44 = v40;
          v43[1] += 8;
        }
      }
      else
      {
        sub_140B2DBD0(a1: v40);
        sub_141750CFC(a1: v40);
      }
      if ( ++v39 >= v63 )
        goto LABEL_91;
    }
    sub_140B2DBD0(a1: v40);
    sub_141750CFC(a1: v40);
    v58 = qword_141B5AD60;
    v61 = nullptr;
    sub_140809040(a1: &v61, a2: 0x14193AAAFLL, a3: 0xFFFFFFFFLL);
    LOBYTE(v59) = 1;
    (*(void (__fastcall **)(__int64, volatile signed __int32 **, __int64, _QWORD))(*(_QWORD *)v58 + 120LL))(
      a1: v58,
      a2: &v61,
      a3: v59,
      a4: 0);
    v54 = v61;
    if ( v61 == nullptr )
      goto LABEL_14;
    goto LABEL_89;
  }
LABEL_91:
  v55 = *(_QWORD *)(qword_141B5AD60 + 8);
  v61 = v62;
  if ( v62 != nullptr )
    _InterlockedIncrement(v62 + 2);
  v56 = (*(__int64 (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v55 + 680LL))(a1: v55, a2: &v61);
  v57 = v61;
  if ( v61 != nullptr && _InterlockedDecrement(v61 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v57)(a1: v57, a2: 1);
  if ( v56 != 0 )
  {
    LOBYTE(a1) = 1;
    goto LABEL_15;
  }
LABEL_14:
  LODWORD(a1) = 0;
LABEL_15:
  v13 = v62;
  if ( v62 != nullptr && _InterlockedDecrement(v62 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v13)(a1: v13, a2: 1);
  return (unsigned int)a1;
}
