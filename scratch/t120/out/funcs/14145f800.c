bool __fastcall sub_14145F800(__int64 a1, _QWORD *a2)
{
  _QWORD *v2; // r12
  _QWORD *v4; // rdi
  _QWORD *v5; // rdi
  __int64 *v6; // r15
  void *v7; // rcx
  int v8; // eax
  __int64 v9; // r13
  __int64 v10; // r12
  __int64 v11; // rsi
  __int64 v12; // r14
  __int64 v13; // rdi
  unsigned __int64 v14; // rcx
  __int64 v15; // r8
  __int64 v16; // rbx
  bool v17; // al
  int v18; // r14d
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 *v21; // r15
  _WORD *v22; // rdi
  __int64 v23; // r13
  unsigned __int64 v24; // rax
  unsigned __int64 v25; // r12
  __int64 v26; // rbx
  _WORD *v27; // rsi
  __int64 v28; // rsi
  unsigned __int64 v29; // rcx
  __int64 v30; // rdi
  __int64 v31; // rdi
  bool v32; // al
  __int64 v33; // rsi
  __int64 v34; // rdi
  __int64 v35; // rdi
  int v36; // esi
  __int64 v37; // rax
  __int64 v38; // rax
  unsigned __int8 *v39; // rdx
  unsigned __int8 *v40; // r14
  __int64 v41; // rsi
  unsigned __int8 *v42; // rbx
  __int64 v44; // rbx
  __int64 v45; // r15
  unsigned __int8 *v46; // rdi
  unsigned __int8 *v47; // r13
  _QWORD *v48; // [rsp+48h] [rbp-38h]
  __int64 v49; // [rsp+50h] [rbp-30h]
  unsigned __int64 v50; // [rsp+58h] [rbp-28h]
  unsigned __int8 *v51; // [rsp+58h] [rbp-28h]
  __int64 v52; // [rsp+60h] [rbp-20h] BYREF
  unsigned __int8 *v53; // [rsp+68h] [rbp-18h]
  __int64 v54; // [rsp+70h] [rbp-10h]
  unsigned __int8 *v55; // [rsp+78h] [rbp-8h]
  int v56; // [rsp+84h] [rbp+4h] BYREF
  unsigned __int8 v57; // [rsp+8Ah] [rbp+Ah] BYREF
  char v58; // [rsp+8Bh] [rbp+Bh] BYREF
  char v59; // [rsp+8Ch] [rbp+Ch] BYREF
  char v60; // [rsp+8Dh] [rbp+Dh] BYREF
  char v61; // [rsp+8Eh] [rbp+Eh] BYREF
  unsigned __int8 v62; // [rsp+8Fh] [rbp+Fh] BYREF
  __int64 v63; // [rsp+90h] [rbp+10h]

  v63 = -2;
  v2 = a2;
  v57 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v57, a3: 1);
  if ( (unsigned __int8)sub_1415F6ED0(a1: a1 + 83, a2: v2) == 0 )
    return false;
  v58 = 0;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v58, a3: 1);
  if ( v58 != 0 )
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
  v59 = 0;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v59, a3: 1);
  if ( v59 != 0 )
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
  v56 = 0;
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v56, a3: 4);
  if ( v56 > 0 )
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
    v6 = (__int64 *)sub_1407E4490(a1: &unk_141B59A68, a2: 24);
    v7 = (void *)qword_141ABD470;
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
      v7 = &unk_141B59A68;
    }
    v48 = v2;
    v6[2] = 0;
    v6[1] = 0;
    *v6 = 0;
    v49 = a1;
    *(_QWORD *)(a1 + 24) = v6;
    v8 = v56;
    v9 = v56;
    v10 = *v6;
    if ( (v6[2] - *v6) >> 1 < (unsigned __int64)v56 )
    {
      if ( v56 < 0 )
        sub_1400526C0();
      v11 = v6[1];
      v12 = sub_1407E4490(a1: v7, a2: 2LL * v56);
      sub_141758A00(a1: v12, a2: *v6, a3: v6[1] - *v6);
      v13 = *v6;
      if ( *v6 != 0 )
      {
        v14 = v6[2] - v13;
        if ( v14 == -1 )
          v14 = *(unsigned int *)(v13 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v15 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v15) >> 3 > v14)
          && (v16 = *(_QWORD *)(v15 + 8 * v14)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v16 + 32, a2: v13 - *(unsigned int *)(v16 + 120));
          v17 = *(_BYTE *)(v16 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 64)) != 0;
          if ( !v17 && *(_BYTE *)(v16 + 97) != 0 )
            sub_1412D33C0(a1: v16);
        }
        else
        {
          MEMORY[0x141948990](a1: v13 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *v6 = v12;
      v6[1] = v12 + v11 - v10;
      v6[2] = v12 + 2 * v9;
      v8 = v56;
    }
    v2 = v48;
    a1 = v49;
    if ( v8 > 0 )
    {
      v18 = 0;
      while ( 1 )
      {
        LOWORD(v52) = 255;
        v19 = *v2;
        (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v52, a3: 1);
        if ( *(_DWORD *)(v19 + 16) != 0 )
          return false;
        v20 = *v2;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: (char *)&v52 + 1, a3: 1);
        if ( *(_DWORD *)(v20 + 16) != 0 )
          return false;
        v21 = *(__int64 **)(a1 + 24);
        v22 = (_WORD *)v21[1];
        if ( v22 == (_WORD *)v21[2] )
          break;
        *v22 = v52;
        v21[1] += 2;
LABEL_34:
        if ( ++v18 >= v56 )
          goto LABEL_59;
      }
      v23 = (__int64)v22 - *v21;
      v24 = v23 >> 1;
      v25 = (v23 >> 1) + ((unsigned __int64)(v23 >> 1) >> 1);
      v50 = (v23 >> 1) + 1;
      if ( v25 <= v50 )
        v25 = v24 + 1;
      if ( v24 > (((unsigned __int64)(((__int64)v22 - *v21) >> 1) >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
        v25 = 0x7FFFFFFFFFFFFFFFLL;
      v26 = sub_1407E4490(a1: qword_141ABD470, a2: 2 * v25);
      *(_WORD *)(v26 + v23) = v52;
      v27 = (_WORD *)v21[1];
      sub_141758A00(a1: v26, a2: *v21, a3: (char *)v22 - *v21);
      if ( v27 != v22 )
        sub_141758A00(a1: v26 + v23 + 2, a2: v22, a3: v21[1] - (_QWORD)v22);
      v28 = *v21;
      a1 = v49;
      if ( *v21 == 0 )
      {
LABEL_54:
        *v21 = v26;
        v21[1] = v26 + 2 * v50;
        v21[2] = v26 + 2 * v25;
        v2 = v48;
        goto LABEL_34;
      }
      v29 = v21[2] - v28;
      if ( v29 == -1 )
      {
        v29 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_53:
          MEMORY[0x141948990](a1: v28 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_54;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_53;
      }
      v30 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29 )
      {
        v31 = *(_QWORD *)(v30 + 8 * v29);
        if ( v31 != 0 )
        {
          MEMORY[0x1419475D8](a1: v31 + 32, a2: v28 - *(unsigned int *)(v31 + 120));
          v32 = *(_BYTE *)(v31 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) != 0;
          if ( !v32 && *(_BYTE *)(v31 + 97) != 0 )
            sub_1412D33C0(a1: v31);
          goto LABEL_54;
        }
      }
      goto LABEL_53;
    }
  }
LABEL_59:
  v60 = 1;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v60, a3: 1);
  if ( v60 != 0 )
  {
    v33 = sub_141750CC0(a1: 6);
    *(_DWORD *)v33 = -65536;
    *(_WORD *)(v33 + 4) = -1;
    *(_QWORD *)(a1 + 32) = v33;
    LOBYTE(v52) = 0;
    v34 = *v2;
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v52, a3: 1);
    if ( *(_DWORD *)(v34 + 16) != 0 )
      return false;
    v35 = *v2;
    if ( *v2 != 0 )
    {
      _InterlockedIncrement((volatile signed __int32 *)(v35 + 8));
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v33 + 4, a3: 1);
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v33, a3: 4);
      (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v35 + 40LL))(a1: v35, a2: v33 + 5, a3: 1);
    }
    v36 = *(_DWORD *)(v35 + 16);
    if ( _InterlockedDecrement((volatile signed __int32 *)(v35 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v35)(a1: v35, a2: 1);
    if ( v36 != 0 )
      return false;
  }
  v61 = 1;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v61, a3: 1);
  if ( v61 != 0 )
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
    v37 = sub_1407E58C0(a1: &unk_141B63FD8, a2: 10);
    *(_DWORD *)v37 = 124518401;
    *(_WORD *)(v37 + 4) = 0;
    *(_DWORD *)(v37 + 6) = -16776961;
    *(_QWORD *)a1 = v37;
    if ( (unsigned __int8)sub_14172A120(a1: v37, a2: v2) == 0 )
      return false;
  }
  if ( (unsigned __int8)sub_14146E9F0(a1: a1 + 62, a2: v2) == 0 )
    return false;
  v38 = *v2;
  v52 = v38;
  if ( v38 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v38 + 8));
  if ( v52 != 0 )
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v52 + 40LL))(a1: v52, a2: a1 + 82, a3: 1);
  v51 = (unsigned __int8 *)(a1 + 82);
  v39 = (unsigned __int8 *)(a1 + 40);
  v40 = (unsigned __int8 *)(a1 + 44);
  if ( v57 < 7u )
  {
    v62 = 0;
    v41 = v52;
    if ( v40 == &v62 )
    {
      v44 = 5;
    }
    else
    {
      v44 = 1;
      if ( v52 != 0 )
        (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v52 + 40LL))(a1: v52, a2: v39, a3: 4);
      v39 = &v62;
    }
    if ( v41 != 0 )
      (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v41 + 40LL))(a1: v41, a2: v39, a3: v44);
    *(_WORD *)(a1 + 78) = v62;
    v42 = (unsigned __int8 *)(a1 + 60);
    v53 = (unsigned __int8 *)(a1 + 60);
    v54 = 2;
    v55 = (unsigned __int8 *)(a1 + 62);
    if ( v41 != 0 )
      goto LABEL_86;
LABEL_87:
    v47 = (unsigned __int8 *)(a1 + 56);
    v53 = v47;
    goto LABEL_88;
  }
  v41 = v52;
  if ( v52 == 0 )
    goto LABEL_87;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v52 + 40LL))(a1: v52, a2: v39, a3: 4);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v41 + 40LL))(a1: v41, a2: a1 + 78, a3: 2);
  v42 = (unsigned __int8 *)(a1 + 60);
  v53 = (unsigned __int8 *)(a1 + 60);
  v54 = 2;
  v55 = (unsigned __int8 *)(a1 + 62);
LABEL_86:
  v45 = a1 + 80;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v41 + 40LL))(a1: v41, a2: v42, a3: 2);
  v53 = (unsigned __int8 *)(a1 + 80);
  v54 = 1;
  v46 = (unsigned __int8 *)(a1 + 81);
  v55 = (unsigned __int8 *)(a1 + 81);
  v47 = (unsigned __int8 *)(a1 + 56);
  (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v41 + 40LL))(a1: v41, a2: v45, a3: 1);
  v53 = v47;
  v54 = 4;
  v55 = v42;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v41 + 40LL))(a1: v41, a2: v47, a3: 4);
  v53 = v46;
  v54 = 1;
  v55 = v51;
  (*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)v41 + 40LL))(a1: v41, a2: v46, a3: 1);
LABEL_88:
  v53 = v40;
  v54 = 12;
  v55 = v47;
  sub_1412E6FF0(a1: &v52);
  return *(_DWORD *)(*v2 + 16LL) == 0;
}
