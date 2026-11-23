int *__fastcall sub_14155DA10(int *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // r13
  __int64 v6; // rdi
  int v7; // eax
  __int64 v8; // r15
  __int64 v9; // r14
  __int64 v10; // r12
  __int64 v11; // rsi
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // rcx
  __int64 v15; // rbx
  __int64 v16; // rcx
  bool v17; // al
  __int64 v18; // rcx
  __int64 *v19; // r15
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rdi
  __int64 v23; // r12
  __int64 v24; // rbx
  __int64 v25; // r13
  __int64 v26; // rsi
  unsigned __int64 v27; // rcx
  __int64 v28; // r8
  __int64 v29; // r14
  bool v30; // al
  __int64 v31; // r12
  __int64 v32; // r14
  __int64 v33; // rsi
  __int64 v34; // rsi
  __int64 v35; // rsi
  __int64 v36; // rsi
  __int64 v37; // rsi
  __int64 v38; // rsi
  __int64 *v39; // rsi
  __int64 v40; // r13
  unsigned __int64 v41; // rax
  unsigned __int64 v42; // rdi
  unsigned __int64 v43; // rcx
  unsigned __int64 v44; // rdi
  __int64 v45; // rbx
  __int64 *v46; // r14
  __int64 v47; // rsi
  unsigned __int64 v48; // rcx
  __int64 v49; // r8
  __int64 v50; // r14
  bool v51; // al
  __int64 *v52; // r12
  __int64 **v53; // rsi
  __int64 v54; // rbx
  unsigned __int64 v55; // rax
  unsigned __int64 v56; // r14
  unsigned __int64 v57; // rcx
  unsigned __int64 v58; // r14
  __int64 v59; // rdi
  __int64 **v60; // r15
  __int64 v61; // rsi
  unsigned __int64 v62; // rcx
  __int64 v63; // r8
  __int64 v64; // r15
  bool v65; // al
  __int64 v66; // rdi
  _QWORD *v67; // rsi
  _QWORD *v68; // rbx
  __int64 v69; // rbx
  unsigned __int64 v70; // rcx
  __int64 v71; // rdx
  __int64 v72; // rdi
  bool v73; // al
  __int64 v75; // [rsp+48h] [rbp-38h]
  int *v76; // [rsp+50h] [rbp-30h]
  _QWORD *v77; // [rsp+58h] [rbp-28h]
  unsigned __int64 v78; // [rsp+60h] [rbp-20h]
  __int64 *v79; // [rsp+68h] [rbp-18h]
  char v80; // [rsp+73h] [rbp-Dh] BYREF
  unsigned int v81; // [rsp+74h] [rbp-Ch] BYREF
  unsigned int v82; // [rsp+78h] [rbp-8h] BYREF
  char v83; // [rsp+7Fh] [rbp-1h] BYREF
  __int64 v84; // [rsp+80h] [rbp+0h]

  v84 = -2;
  v4 = a2;
  v82 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v82, a3: 4);
  v6 = v82;
  v7 = 1;
  if ( qword_141AA7808 <= (unsigned __int64)v82 )
    goto LABEL_125;
  v76 = a1;
  v8 = *a3;
  v79 = a3;
  if ( (a3[2] - *a3) >> 3 >= (unsigned __int64)v82 )
    goto LABEL_14;
  v9 = a3[1];
  v10 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v82);
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
        v15 = v14;
        MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
        v16 = v15;
        v17 = *(_BYTE *)(v15 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) != 0;
        a3 = v79;
        if ( !v17 && *(_BYTE *)(v16 + 97) != 0 )
          sub_1412D33C0(a1: v16);
        goto LABEL_13;
      }
    }
    goto LABEL_12;
  }
LABEL_13:
  *a3 = v10;
  a3[1] = v10 + v9 - v8;
  a3[2] = v10 + 8 * v6;
  LODWORD(v6) = v82;
LABEL_14:
  if ( (_DWORD)v6 == 0 )
  {
LABEL_111:
    v7 = *(_DWORD *)(*v4 + 16LL);
    a1 = v76;
    goto LABEL_125;
  }
  v18 = 0;
  v77 = v4;
  while ( 1 )
  {
    v75 = v18;
    if ( dword_141B5E2A8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5E2A8);
      if ( dword_141B5E2A8 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5E258,
          a2: 1100123086,
          a3: 1024,
          a4: 32,
          a5: 0,
          a6: 0,
          a7: 1024,
          a8: 4096);
        sub_141751048(a1: sub_140ED17E0);
        sub_141750EA0(a1: &dword_141B5E2A8);
      }
    }
    v19 = (__int64 *)sub_1407E58C0(a1: &unk_141B5E258, a2: 32);
    *v19 = 0;
    v19[1] = 0;
    v19[2] = 0;
    v19[3] = 0;
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
    v19[2] = 0;
    v19[1] = 0;
    *v19 = 0;
    *((_BYTE *)v19 + 24) = 1;
    v20 = *v4;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v83, a3: 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      break;
    v21 = *v4;
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v19 + 3, a3: 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      break;
    v81 = 0;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v81, a3: 4);
    v22 = v81;
    if ( qword_141AA7808 <= (unsigned __int64)v81 )
      break;
    v23 = *v19;
    if ( (v19[2] - *v19) >> 3 >= (unsigned __int64)v81 )
      goto LABEL_35;
    v24 = v19[1];
    v25 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v81);
    sub_141758A00(a1: v25, a2: *v19, a3: v19[1] - *v19);
    v26 = *v19;
    if ( *v19 != 0 )
    {
      v27 = v19[2] - v26;
      if ( v27 == -1 )
      {
        v27 = *(unsigned int *)(v26 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_33:
          MEMORY[0x141948990](a1: v26 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_34;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_33;
      }
      v28 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v28) >> 3 > v27 )
      {
        v29 = *(_QWORD *)(v28 + 8 * v27);
        if ( v29 != 0 )
        {
          MEMORY[0x1419475D8](a1: v29 + 32, a2: v26 - *(unsigned int *)(v29 + 120));
          v30 = *(_BYTE *)(v29 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) != 0;
          if ( !v30 && *(_BYTE *)(v29 + 97) != 0 )
            sub_1412D33C0(a1: v29);
          goto LABEL_34;
        }
      }
      goto LABEL_33;
    }
LABEL_34:
    *v19 = v25;
    v19[1] = v25 + v24 - v23;
    v19[2] = v25 + 8 * v22;
    LODWORD(v22) = v81;
    v4 = v77;
LABEL_35:
    if ( (_DWORD)v22 != 0 )
    {
      v31 = 0;
      while ( 1 )
      {
        if ( dword_141B5E250 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5E250);
          if ( dword_141B5E250 == -1 )
          {
            sub_1407E53D0(
              a1: (unsigned int)&unk_141B5E200,
              a2: 1100123091,
              a3: 1024,
              a4: 12,
              a5: 0,
              a6: 0,
              a7: 1024,
              a8: 0);
            sub_141751048(a1: sub_140ED17D0);
            sub_141750EA0(a1: &dword_141B5E250);
          }
        }
        v32 = sub_1407E58C0(a1: &unk_141B5E200, a2: 12);
        *(_DWORD *)(v32 + 8) = 65792;
        *(_QWORD *)v32 = -1;
        v33 = *v4;
        (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v80, a3: 1);
        if ( *(_DWORD *)(v33 + 16) != 0 )
          goto LABEL_105;
        v34 = *v4;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v32 + 8, a3: 1);
        if ( *(_DWORD *)(v34 + 16) != 0 )
          goto LABEL_105;
        v35 = *v4;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v32 + 10, a3: 1);
        if ( *(_DWORD *)(v35 + 16) != 0
          || (v36 = *v4,
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v32 + 9, a3: 1),
              *(_DWORD *)(v36 + 16) != 0)
          || (v37 = *v4,
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v32 + 4, a3: 4),
              *(_DWORD *)(v37 + 16) != 0)
          || (v38 = *v4,
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v32, a3: 4),
              *(_DWORD *)(v38 + 16) != 0) )
        {
LABEL_105:
          sub_14155D8A0(a1: v32);
          goto LABEL_106;
        }
        if ( *(_DWORD *)(*v4 + 16LL) != 0 )
        {
          sub_14155D8A0(a1: v32);
          goto LABEL_72;
        }
        v39 = (__int64 *)v19[1];
        if ( v39 == (__int64 *)v19[2] )
          break;
        *v39 = v32;
        v19[1] += 8;
LABEL_38:
        if ( ++v31 >= (unsigned __int64)v81 )
          goto LABEL_72;
      }
      v40 = (__int64)v39 - *v19;
      v41 = v40 >> 3;
      v42 = (unsigned __int64)(v40 >> 3) >> 1;
      v43 = 0x1FFFFFFFFFFFFFFFLL - v42;
      v44 = (v40 >> 3) + v42;
      v78 = (v40 >> 3) + 1;
      if ( v44 <= v78 )
        v44 = v41 + 1;
      if ( v41 > v43 )
        v44 = 0x1FFFFFFFFFFFFFFFLL;
      v45 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v44);
      *(_QWORD *)(v45 + v40) = v32;
      v46 = (__int64 *)v19[1];
      sub_141758A00(a1: v45, a2: *v19, a3: (char *)v39 - *v19);
      if ( v46 != v39 )
        sub_141758A00(a1: v45 + v40 + 8, a2: v39, a3: v19[1] - (_QWORD)v39);
      v47 = *v19;
      v4 = v77;
      if ( *v19 != 0 )
      {
        v48 = v19[2] - v47;
        if ( v48 == -1 )
        {
          v48 = *(unsigned int *)(v47 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_63;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_63;
        }
        v49 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v49) >> 3 > v48 && (v50 = *(_QWORD *)(v49 + 8 * v48)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v50 + 32, a2: v47 - *(unsigned int *)(v50 + 120));
          v51 = *(_BYTE *)(v50 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v50 + 64)) != 0;
          if ( !v51 && *(_BYTE *)(v50 + 97) != 0 )
            sub_1412D33C0(a1: v50);
        }
        else
        {
LABEL_63:
          MEMORY[0x141948990](a1: v47 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      *v19 = v45;
      v19[1] = v45 + 8 * v78;
      v19[2] = v45 + 8 * v44;
      goto LABEL_38;
    }
LABEL_72:
    v52 = v79;
    if ( *(_DWORD *)(*v4 + 16LL) != 0 )
      break;
    v53 = (__int64 **)v79[1];
    if ( v53 == (__int64 **)v79[2] )
    {
      v54 = (__int64)v53 - *v79;
      v55 = v54 >> 3;
      v56 = (unsigned __int64)(v54 >> 3) >> 1;
      v57 = 0x1FFFFFFFFFFFFFFFLL - v56;
      v58 = (v54 >> 3) + v56;
      if ( v58 <= (v54 >> 3) + 1 )
        v58 = v55 + 1;
      if ( v55 > v57 )
        v58 = 0x1FFFFFFFFFFFFFFFLL;
      v59 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v58);
      *(_QWORD *)(v59 + v54) = v19;
      v60 = (__int64 **)v79[1];
      sub_141758A00(a1: v59, a2: *v79, a3: (char *)v53 - *v79);
      if ( v60 != v53 )
        sub_141758A00(a1: v59 + v54 + 8, a2: v53, a3: v79[1] - (_QWORD)v53);
      v61 = *v79;
      if ( *v79 != 0 )
      {
        v62 = v79[2] - v61;
        if ( v62 == -1 )
          v62 = *(unsigned int *)(v61 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v63 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v63) >> 3 > v62)
          && (v64 = *(_QWORD *)(v63 + 8 * v62)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v64 + 32, a2: v61 - *(unsigned int *)(v64 + 120));
          v65 = *(_BYTE *)(v64 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v64 + 64)) != 0;
          v52 = v79;
          if ( !v65 && *(_BYTE *)(v64 + 97) != 0 )
            sub_1412D33C0(a1: v64);
        }
        else
        {
          MEMORY[0x141948990](a1: v61 - *(unsigned int *)(qword_141ABD470 + 48));
          v52 = v79;
        }
      }
      *v52 = v59;
      v52[1] = v59 + 8 * ((v54 >> 3) + 1);
      v52[2] = v59 + 8 * v58;
    }
    else
    {
      *v53 = v19;
      v79[1] += 8;
    }
    v18 = v75 + 1;
    if ( v75 + 1 >= (unsigned __int64)v82 )
      goto LABEL_111;
  }
LABEL_106:
  v66 = *v19;
  v67 = (_QWORD *)v19[1];
  if ( (_QWORD *)*v19 != v67 )
  {
    v68 = (_QWORD *)*v19;
    do
    {
      if ( *v68 != 0 )
        sub_14155D8A0(a1: *v68);
      ++v68;
    }
    while ( v68 != v67 );
    v69 = v19[1] - (_QWORD)v67;
    sub_141758A00(a1: v66, a2: v67, a3: v69);
    v19[1] = v66 + v69;
    v67 = (_QWORD *)*v19;
  }
  if ( v67 != nullptr )
  {
    v70 = v19[2] - (_QWORD)v67;
    if ( v70 == -1 )
    {
      v70 = *(unsigned int *)((char *)v67 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_122;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_122;
    }
    v71 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v71) >> 3 > v70 && (v72 = *(_QWORD *)(v71 + 8 * v70)) != 0 )
    {
      MEMORY[0x1419475D8](a1: v72 + 32, a2: (char *)v67 - *(unsigned int *)(v72 + 120));
      v73 = *(_BYTE *)(v72 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v72 + 64)) != 0;
      if ( !v73 && *(_BYTE *)(v72 + 97) != 0 )
        sub_1412D33C0(a1: v72);
    }
    else
    {
LABEL_122:
      MEMORY[0x141948990](a1: (char *)v67 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v19[2] = 0;
    v19[1] = 0;
    *v19 = 0;
  }
  sub_140ED1660(a1: v19);
  a1 = v76;
  v7 = 1;
LABEL_125:
  *a1 = v7;
  return a1;
}
