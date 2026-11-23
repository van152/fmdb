bool __fastcall sub_14145F800(__int64 a1, __int64 *a2)
{
  __int64 *v2; // r12
  _QWORD *v4; // rdi
  _QWORD *v5; // rdi
  __int64 v6; // r8
  __int64 *v7; // r15
  void *v8; // rcx
  int v9; // eax
  __int64 v10; // r13
  __int64 v11; // r12
  unsigned __int64 v12; // rdx
  __int64 v13; // rsi
  __int64 v14; // r14
  __int64 v15; // rdi
  unsigned __int64 v16; // rcx
  __int64 v17; // r8
  __int64 v18; // rbx
  bool v19; // al
  int v20; // r14d
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 *v23; // r15
  _WORD *v24; // rdi
  __int64 v25; // r13
  unsigned __int64 v26; // rax
  unsigned __int64 v27; // r12
  __int64 v28; // rbx
  _WORD *v29; // rsi
  __int64 v30; // rsi
  unsigned __int64 v31; // rcx
  __int64 v32; // rdi
  __int64 v33; // rdi
  bool v34; // al
  __int64 v35; // rsi
  __int64 v36; // rdi
  __int64 v37; // rdi
  int v38; // esi
  __int64 v39; // rax
  __int64 v40; // rax
  unsigned __int8 *v41; // rdx
  unsigned __int8 *v42; // r14
  __int64 v43; // rsi
  unsigned __int8 *v44; // rbx
  __int64 v46; // rbx
  __int64 v47; // r15
  unsigned __int8 *v48; // rdi
  unsigned __int8 *v49; // r13
  __int64 *v50; // [rsp+48h] [rbp-38h]
  __int64 v51; // [rsp+50h] [rbp-30h]
  unsigned __int64 v52; // [rsp+58h] [rbp-28h]
  unsigned __int8 *v53; // [rsp+58h] [rbp-28h]
  __int64 v54; // [rsp+60h] [rbp-20h] BYREF
  unsigned __int8 *v55; // [rsp+68h] [rbp-18h]
  __int64 v56; // [rsp+70h] [rbp-10h]
  unsigned __int8 *v57; // [rsp+78h] [rbp-8h]
  int v58; // [rsp+84h] [rbp+4h] BYREF
  unsigned __int8 v59; // [rsp+8Ah] [rbp+Ah] BYREF
  char v60; // [rsp+8Bh] [rbp+Bh] BYREF
  char v61; // [rsp+8Ch] [rbp+Ch] BYREF
  char v62; // [rsp+8Dh] [rbp+Dh] BYREF
  char v63; // [rsp+8Eh] [rbp+Eh] BYREF
  unsigned __int8 v64; // [rsp+8Fh] [rbp+Fh] BYREF
  __int64 v65; // [rsp+90h] [rbp+10h]

  v65 = -2;
  v2 = a2;
  v59 = 0;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v59, a3: 1);
  if ( (unsigned __int8)sub_1415F6ED0(a1: a1 + 83, a2: v2) == 0 )
    return false;
  v60 = 0;
  (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v60, a3: 1);
  if ( v60 != 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    v4 = (_QWORD *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
    if ( qword_141ABD470 == 0 )
    {
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v4[2] = 0;
    v4[1] = 0;
    *v4 = 0;
    *(_QWORD *)(a1 + 8) = v4;
    if ( (unsigned __int8)sub_14172A440(a1: v4, a2: v2) == 0 )
      return false;
  }
  v61 = 0;
  (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v61, a3: 1);
  if ( v61 != 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    v5 = (_QWORD *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
    if ( qword_141ABE200 == 0 )
    {
      if ( dword_141B59AF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AF0);
        if ( dword_141B59AF0 == -1 )
        {
          sub_1407E5B40(a1: &unk_141B59AB0);
          sub_141751048(a1: sub_1407E6720);
          sub_141750EA0(a1: &dword_141B59AF0);
        }
      }
      qword_141ABE200 = (__int64)&unk_141B59AB0;
    }
    v5[2] = 0;
    v5[1] = 0;
    *v5 = 0;
    *(_QWORD *)(a1 + 16) = v5;
    if ( (unsigned __int8)sub_14145E300(a1: v5, a2: v2) == 0 )
      return false;
  }
  v58 = 0;
  (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v58, a3: 4);
  if ( v58 > 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    v7 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
    v8 = (void *)qword_141ABD470;
    if ( qword_141ABD470 == 0 )
    {
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      qword_141ABD470 = (__int64)&unk_141B59A68;
      v8 = &unk_141B59A68;
    }
    v50 = v2;
    v7[2] = 0;
    v7[1] = 0;
    *v7 = 0;
    v51 = a1;
    *(_QWORD *)(a1 + 24) = v7;
    v9 = v58;
    v10 = v58;
    v11 = *v7;
    v12 = (v7[2] - *v7) >> 1;
    if ( v12 < v58 )
    {
      if ( v58 < 0 )
        sub_1400526C0(a1: v8, a2: v12, a3: v6);
      v13 = v7[1];
      v14 = sub_1407E4490(a1: v8, a2: 2LL * v58);
      sub_141758A00(a1: v14, a2: *v7, a3: v7[1] - *v7);
      v15 = *v7;
      if ( *v7 != 0 )
      {
        v16 = v7[2] - v15;
        if ( v16 == -1 )
          v16 = *(unsigned int *)(v15 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v17 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v17) >> 3 > v16)
          && (v18 = *(_QWORD *)(v17 + 8 * v16)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v18 + 32, a2: v15 - *(unsigned int *)(v18 + 120));
          v19 = *(_BYTE *)(v18 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 64)) != 0;
          if ( !v19 && *(_BYTE *)(v18 + 97) != 0 )
            sub_1412D33C0(a1: v18);
        }
        else
        {
          MEMORY[0x141948990](a1: v15 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *v7 = v14;
      v7[1] = v14 + v13 - v11;
      v7[2] = v14 + 2 * v10;
      v9 = v58;
    }
    v2 = v50;
    a1 = v51;
    if ( v9 > 0 )
    {
      v20 = 0;
      while ( 1 )
      {
        LOWORD(v54) = 255;
        v21 = *v2;
        (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v54, a3: 1);
        if ( *(_DWORD *)(v21 + 16) != 0 )
          return false;
        v22 = *v2;
        (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: (char *)&v54 + 1, a3: 1);
        if ( *(_DWORD *)(v22 + 16) != 0 )
          return false;
        v23 = *(__int64 **)(a1 + 24);
        v24 = (_WORD *)v23[1];
        if ( v24 == (_WORD *)v23[2] )
          break;
        *v24 = v54;
        v23[1] += 2;
LABEL_34:
        if ( ++v20 >= v58 )
          goto LABEL_59;
      }
      v25 = (__int64)v24 - *v23;
      v26 = v25 >> 1;
      v27 = (v25 >> 1) + ((unsigned __int64)(v25 >> 1) >> 1);
      v52 = (v25 >> 1) + 1;
      if ( v27 <= v52 )
        v27 = v26 + 1;
      if ( v26 > (((unsigned __int64)(((__int64)v24 - *v23) >> 1) >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
        v27 = 0x7FFFFFFFFFFFFFFFLL;
      v28 = sub_1407E4490(a1: qword_141ABD470, a2: 2 * v27);
      *(_WORD *)(v28 + v25) = v54;
      v29 = (_WORD *)v23[1];
      sub_141758A00(a1: v28, a2: *v23, a3: (char *)v24 - *v23);
      if ( v29 != v24 )
        sub_141758A00(a1: v28 + v25 + 2, a2: v24, a3: v23[1] - (_QWORD)v24);
      v30 = *v23;
      a1 = v51;
      if ( *v23 == 0 )
      {
LABEL_54:
        *v23 = v28;
        v23[1] = v28 + 2 * v52;
        v23[2] = v28 + 2 * v27;
        v2 = v50;
        goto LABEL_34;
      }
      v31 = v23[2] - v30;
      if ( v31 == -1 )
      {
        v31 = *(unsigned int *)(v30 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_53:
          MEMORY[0x141948990](a1: v30 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_54;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_53;
      }
      v32 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v32) >> 3 > v31 )
      {
        v33 = *(_QWORD *)(v32 + 8 * v31);
        if ( v33 != 0 )
        {
          MEMORY[0x1419475D8](a1: v33 + 32, a2: v30 - *(unsigned int *)(v33 + 120));
          v34 = *(_BYTE *)(v33 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v33 + 64)) != 0;
          if ( !v34 && *(_BYTE *)(v33 + 97) != 0 )
            sub_1412D33C0(a1: v33);
          goto LABEL_54;
        }
      }
      goto LABEL_53;
    }
  }
LABEL_59:
  v62 = 1;
  (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v62, a3: 1);
  if ( v62 != 0 )
  {
    v35 = sub_141750CC0(a1: 6);
    *(_DWORD *)v35 = -65536;
    *(_WORD *)(v35 + 4) = -1;
    *(_QWORD *)(a1 + 32) = v35;
    LOBYTE(v54) = 0;
    v36 = *v2;
    (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v54, a3: 1);
    if ( *(_DWORD *)(v36 + 16) != 0 )
      return false;
    v37 = *v2;
    if ( *v2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v37 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v37 + 40LL))(a1: v37, a2: v35 + 4, a3: 1);
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v37 + 40LL))(a1: v37, a2: v35, a3: 4);
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v37 + 40LL))(a1: v37, a2: v35 + 5, a3: 1);
    }
    v38 = *(_DWORD *)(v37 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v37 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v37)(a1: v37, a2: 1);
    if ( v38 != 0 )
      return false;
  }
  v63 = 1;
  (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v63, a3: 1);
  if ( v63 != 0 )
  {
    if ( dword_141B64028 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B64028);
      if ( dword_141B64028 == -1 )
      {
        sub_1407E53D0(a1: (unsigned int)&unk_141B63FD8, a2: 1100137940, a3: 1024, a4: 10, a5: 0, a6: 0, a7: 1024, a8: 0);
        sub_141751048(a1: sub_1414609C0);
        sub_141750EA0(a1: &dword_141B64028);
      }
    }
    v39 = sub_1407E58C0(a1: &unk_141B63FD8, a2: 10);
    *(_DWORD *)v39 = 124518401;
    *(_WORD *)(v39 + 4) = 0;
    *(_DWORD *)(v39 + 6) = -16776961;
    *(_QWORD *)a1 = v39;
    if ( (unsigned __int8)sub_14172A120(a1: v39, a2: v2) == 0 )
      return false;
  }
  if ( (unsigned __int8)sub_14146E9F0(a1: a1 + 62, a2: v2) == 0 )
    return false;
  v40 = *v2;
  v54 = v40;
  if ( v40 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v40 + 8));
  if ( v54 != 0 )
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v54 + 40LL))(a1: v54, a2: a1 + 82, a3: 1);
  v53 = (unsigned __int8 *)(a1 + 82);
  v41 = (unsigned __int8 *)(a1 + 40);
  v42 = (unsigned __int8 *)(a1 + 44);
  if ( v59 < 7u )
  {
    v64 = 0;
    v43 = v54;
    if ( v42 == &v64 )
    {
      v46 = 5;
    }
    else
    {
      v46 = 1;
      if ( v54 != 0 )
        (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v54 + 40LL))(a1: v54, a2: v41, a3: 4);
      v41 = &v64;
    }
    if ( v43 != 0 )
      (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v43 + 40LL))(a1: v43, a2: v41, a3: v46);
    *(_WORD *)(a1 + 78) = v64;
    v44 = (unsigned __int8 *)(a1 + 60);
    v55 = (unsigned __int8 *)(a1 + 60);
    v56 = 2;
    v57 = (unsigned __int8 *)(a1 + 62);
    if ( v43 != 0 )
      goto LABEL_86;
LABEL_87:
    v49 = (unsigned __int8 *)(a1 + 56);
    v55 = v49;
    goto LABEL_88;
  }
  v43 = v54;
  if ( v54 == 0 )
    goto LABEL_87;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v54 + 40LL))(a1: v54, a2: v41, a3: 4);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v43 + 40LL))(a1: v43, a2: a1 + 78, a3: 2);
  v44 = (unsigned __int8 *)(a1 + 60);
  v55 = (unsigned __int8 *)(a1 + 60);
  v56 = 2;
  v57 = (unsigned __int8 *)(a1 + 62);
LABEL_86:
  v47 = a1 + 80;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v43 + 40LL))(a1: v43, a2: v44, a3: 2);
  v55 = (unsigned __int8 *)(a1 + 80);
  v56 = 1;
  v48 = (unsigned __int8 *)(a1 + 81);
  v57 = (unsigned __int8 *)(a1 + 81);
  v49 = (unsigned __int8 *)(a1 + 56);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v43 + 40LL))(a1: v43, a2: v47, a3: 1);
  v55 = v49;
  v56 = 4;
  v57 = v44;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v43 + 40LL))(a1: v43, a2: v49, a3: 4);
  v55 = v48;
  v56 = 1;
  v57 = v53;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v43 + 40LL))(a1: v43, a2: v48, a3: 1);
LABEL_88:
  v55 = v42;
  v56 = 12;
  v57 = v49;
  sub_1412E6FF0(a1: &v54);
  return *(_DWORD *)(*v2 + 16) == 0;
}
