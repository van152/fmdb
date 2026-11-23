int *__fastcall sub_14155CB20(int *a1, _QWORD *a2, __int64 *a3)
{
  __int64 v6; // rsi
  int v7; // eax
  __int64 v8; // r15
  __int64 v9; // rdi
  __int64 v10; // r12
  __int64 v11; // rbp
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // rdi
  __int64 v17; // r12
  __int64 v18; // rbp
  __int64 v19; // rbp
  __int64 v20; // rbp
  __int64 v21; // rbp
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 *v26; // r14
  __int64 v27; // r15
  unsigned __int64 v28; // rax
  unsigned __int64 v29; // rbp
  __int64 v30; // rax
  __int64 v31; // r12
  __int64 *v32; // rsi
  __int64 v33; // rsi
  unsigned __int64 v34; // rcx
  __int64 v35; // r8
  __int64 v36; // r14
  bool v37; // al
  unsigned __int8 v39; // [rsp+49h] [rbp-5Fh] BYREF
  __int16 v40; // [rsp+4Ah] [rbp-5Eh] BYREF
  unsigned int v41; // [rsp+4Ch] [rbp-5Ch] BYREF
  int *v42; // [rsp+50h] [rbp-58h]
  __int64 v43; // [rsp+58h] [rbp-50h]
  unsigned __int64 v44; // [rsp+60h] [rbp-48h]

  v41 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v41, a3: 4);
  v6 = v41;
  v7 = 1;
  if ( qword_141AA7808 <= (unsigned __int64)v41 )
    goto LABEL_59;
  v42 = a1;
  v8 = *a3;
  if ( (a3[2] - *a3) >> 3 >= (unsigned __int64)v41 )
    goto LABEL_14;
  v9 = a3[1];
  v10 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v41);
  sub_141758A00(a1: v10, a2: *a3, a3: a3[1] - *a3);
  v11 = *a3;
  if ( *a3 != 0 )
  {
    v12 = a3[2] - v11;
    if ( v12 == -1 )
    {
      v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_12:
        MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_13;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_12;
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12 )
    {
      v14 = *(_QWORD *)(v13 + 8 * v12);
      if ( v14 != 0 )
      {
        MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
        v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
        if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
          sub_1412D33C0(a1: v14);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_13:
  *a3 = v10;
  a3[1] = v10 + v9 - v8;
  a3[2] = v10 + 8 * v6;
  LODWORD(v6) = v41;
LABEL_14:
  if ( (_DWORD)v6 == 0 )
    goto LABEL_58;
  v16 = 0;
  while ( 1 )
  {
    if ( dword_141B5E1A0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5E1A0);
      if ( dword_141B5E1A0 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5E150,
          a2: 1100122013,
          a3: 0x4000,
          a4: 12,
          a5: 0,
          a6: 0,
          a7: 1024,
          a8: 0);
        sub_141751048(a1: sub_140ED1650);
        sub_141750EA0(a1: &dword_141B5E1A0);
      }
    }
    v17 = sub_1407E58C0(a1: &unk_141B5E150, a2: 12);
    *(_QWORD *)v17 = 0xFF00FFFFFFFFLL;
    *(_WORD *)(v17 + 8) = 0;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v40, a3: 2);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      goto LABEL_56;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17, a3: 4);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      goto LABEL_56;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17 + 4, a3: 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      goto LABEL_56;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17 + 5, a3: 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      goto LABEL_56;
    if ( v40 < 2 )
    {
      v23 = *a2;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v39, a3: 1);
      if ( *(_DWORD *)(v23 + 16) != 0 )
        goto LABEL_56;
      *(_WORD *)(v17 + 6) = v39;
    }
    else
    {
      v22 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17 + 6, a3: 2);
      if ( *(_DWORD *)(v22 + 16) != 0 )
        goto LABEL_56;
    }
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17 + 8, a3: 1);
    if ( *(_DWORD *)(v24 + 16) != 0
      || v40 >= 3
      && (v25 = *a2,
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v17 + 9, a3: 1),
          *(_DWORD *)(v25 + 16) != 0) )
    {
LABEL_56:
      sub_140ED14E0(a1: v17);
      a1 = v42;
      v7 = 1;
      goto LABEL_59;
    }
    if ( *(_DWORD *)(*a2 + 16LL) != 0 )
      break;
    v26 = (__int64 *)a3[1];
    if ( v26 == (__int64 *)a3[2] )
    {
      v43 = v16;
      v27 = (__int64)v26 - *a3;
      v28 = v27 >> 3;
      v29 = v28 + (v28 >> 1);
      v44 = (v27 >> 3) + 1;
      if ( v29 <= v44 )
        v29 = v28 + 1;
      if ( v28 > 0x1FFFFFFFFFFFFFFFLL - (v28 >> 1) )
        v29 = 0x1FFFFFFFFFFFFFFFLL;
      v30 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v29);
      *(_QWORD *)(v30 + v27) = v17;
      v31 = v30;
      v32 = (__int64 *)a3[1];
      sub_141758A00(a1: v30, a2: *a3, a3: (char *)v26 - *a3);
      if ( v32 != v26 )
        sub_141758A00(a1: v31 + v27 + 8, a2: v26, a3: a3[1] - (_QWORD)v26);
      v33 = *a3;
      v16 = v43;
      if ( *a3 != 0 )
      {
        v34 = a3[2] - v33;
        if ( v34 == -1 )
        {
          v34 = *(unsigned int *)(v33 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_48;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_48;
        }
        v35 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v35) >> 3 > v34 && (v36 = *(_QWORD *)(v35 + 8 * v34)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v36 + 32, a2: v33 - *(unsigned int *)(v36 + 120));
          v37 = *(_BYTE *)(v36 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 64)) != 0;
          if ( !v37 && *(_BYTE *)(v36 + 97) != 0 )
            sub_1412D33C0(a1: v36);
        }
        else
        {
LABEL_48:
          MEMORY[0x141948990](a1: v33 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *a3 = v31;
      a3[1] = v31 + 8 * v44;
      a3[2] = v31 + 8 * v29;
      goto LABEL_17;
    }
    *v26 = v17;
    a3[1] += 8;
LABEL_17:
    if ( ++v16 >= (unsigned __int64)v41 )
      goto LABEL_58;
  }
  sub_140ED14E0(a1: v17);
LABEL_58:
  v7 = *(_DWORD *)(*a2 + 16LL);
  a1 = v42;
LABEL_59:
  *a1 = v7;
  return a1;
}
