char __fastcall sub_140E93BD0(_QWORD *a1, __int64 *a2)
{
  void *v4; // rcx
  __int64 v5; // rsi
  __int64 v6; // r13
  _QWORD *v7; // r14
  _QWORD **v8; // rsi
  _QWORD **v9; // r15
  _QWORD *v10; // r12
  _QWORD *v11; // rbx
  _QWORD *v12; // rdi
  __int64 v13; // rcx
  __int64 v14; // r12
  unsigned __int64 v15; // rbx
  unsigned __int64 v16; // r14
  unsigned __int64 v17; // rcx
  unsigned __int64 v18; // r14
  __int64 v19; // r15
  __int64 v20; // r12
  unsigned __int64 v21; // r15
  unsigned __int64 v22; // rdi
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // rdi
  __int64 v25; // r14
  __int64 v26; // rcx
  __int64 v27; // rdi
  __int64 v28; // rcx
  __int64 v29; // rbx
  __int64 v30; // rcx
  __int64 v31; // rdx
  unsigned __int64 v32; // rdi
  __int64 v33; // r14
  __int64 v34; // r15
  __int64 v35; // rsi
  unsigned __int64 v36; // rcx
  __int64 v37; // r8
  __int64 v38; // rcx
  __int64 v39; // rbx
  __int64 v40; // rsi
  __int64 v41; // rdi
  __int64 v42; // rax
  __int64 v43; // rcx
  _QWORD **v44; // rbx
  __int64 v45; // rax
  __int64 v46; // rcx
  char result; // al
  _QWORD *v48; // rsi
  unsigned __int64 v49; // rbx
  __int64 v50; // rcx
  __int64 v51; // rsi
  signed __int32 v52; // et0
  __int64 *v53; // [rsp+20h] [rbp-40h]
  __int64 v54; // [rsp+28h] [rbp-38h]
  __int64 v55; // [rsp+30h] [rbp-30h] BYREF
  __int64 v56; // [rsp+38h] [rbp-28h]
  unsigned __int64 v57; // [rsp+40h] [rbp-20h]
  __int64 v58; // [rsp+48h] [rbp-18h] BYREF
  __int64 v59; // [rsp+50h] [rbp-10h]
  _QWORD **v60; // [rsp+58h] [rbp-8h]
  __int64 v61; // [rsp+60h] [rbp+0h]

  v61 = -2;
  v4 = (void *)qword_141ABD470;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    v4 = &unk_141B59A68;
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v5 = a1[1] - *a1;
  v53 = a2;
  if ( v5 != 0 )
  {
    if ( v5 < 0 )
      sub_1400526C0(v4);
    v6 = sub_1407E4490(v4, v5);
    v7 = (_QWORD *)(v6 + 8 * (v5 >> 3));
    v8 = (_QWORD **)*a1;
    v9 = (_QWORD **)a1[1];
    v10 = (_QWORD *)v6;
    if ( (_QWORD **)*a1 != v9 )
    {
      v60 = (_QWORD **)a1[1];
      do
      {
        v11 = *v8;
        if ( *v8 != nullptr )
        {
          v12 = (_QWORD *)sub_141750CC0(16);
          v13 = v11[1];
          *v12 = *v11;
          v12[1] = v13;
          if ( v10 == v7 )
          {
            v14 = (__int64)v10 - v6;
            v15 = (v14 >> 3) + 1;
            v16 = (unsigned __int64)(v14 >> 3) >> 1;
            v17 = 0x1FFFFFFFFFFFFFFFLL - v16;
            v18 = (v14 >> 3) + v16;
            if ( v18 <= v15 )
              v18 = (v14 >> 3) + 1;
            if ( v14 >> 3 > v17 )
              v18 = 0x1FFFFFFFFFFFFFFFLL;
            v19 = sub_1407E4490(qword_141ABD470, 8 * v18);
            *(_QWORD *)(v19 + v14) = v12;
            sub_141758A00();
            if ( v6 != 0 )
            {
              if ( v14 == -1 )
              {
                v14 = *(unsigned int *)(v6 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                  goto LABEL_37;
              }
              else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              {
                goto LABEL_37;
              }
              v26 = *(_QWORD *)(qword_141ABD470 + 24);
              if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > (unsigned __int64)v14
                && (v27 = *(_QWORD *)(v26 + 8 * v14)) != 0 )
              {
                MEMORY[0x1419475D8](v27 + 32, v6 - *(unsigned int *)(v27 + 120));
                if ( (*(_BYTE *)(v27 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) == 0)
                  && *(_BYTE *)(v27 + 97) != 0 )
                {
                  sub_1412D33C0(v27);
                }
              }
              else
              {
LABEL_37:
                MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            v10 = (_QWORD *)(v19 + 8 * v15);
            v7 = (_QWORD *)(v19 + 8 * v18);
            v6 = v19;
            goto LABEL_47;
          }
          *v10 = v12;
        }
        else
        {
          if ( v10 == v7 )
          {
            v20 = (__int64)v10 - v6;
            v21 = (v20 >> 3) + 1;
            v22 = (unsigned __int64)(v20 >> 3) >> 1;
            v23 = 0x1FFFFFFFFFFFFFFFLL - v22;
            v24 = (v20 >> 3) + v22;
            if ( v24 <= v21 )
              v24 = (v20 >> 3) + 1;
            if ( v20 >> 3 > v23 )
              v24 = 0x1FFFFFFFFFFFFFFFLL;
            v25 = sub_1407E4490(qword_141ABD470, 8 * v24);
            *(_QWORD *)(v25 + v20) = 0;
            sub_141758A00();
            if ( v6 != 0 )
            {
              if ( v20 == -1 )
              {
                v20 = *(unsigned int *)(v6 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                  goto LABEL_45;
              }
              else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
              {
                goto LABEL_45;
              }
              v28 = *(_QWORD *)(qword_141ABD470 + 24);
              if ( (*(_QWORD *)(qword_141ABD470 + 32) - v28) >> 3 > (unsigned __int64)v20
                && (v29 = *(_QWORD *)(v28 + 8 * v20)) != 0 )
              {
                MEMORY[0x1419475D8](v29 + 32, v6 - *(unsigned int *)(v29 + 120));
                if ( (*(_BYTE *)(v29 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) == 0)
                  && *(_BYTE *)(v29 + 97) != 0 )
                {
                  sub_1412D33C0(v29);
                }
              }
              else
              {
LABEL_45:
                MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            v10 = (_QWORD *)(v25 + 8 * v21);
            v6 = v25;
            v7 = (_QWORD *)(v25 + 8 * v24);
LABEL_47:
            v9 = v60;
            goto LABEL_10;
          }
          *v10 = 0;
        }
        ++v10;
LABEL_10:
        ++v8;
      }
      while ( v8 != v9 );
    }
  }
  else
  {
    v6 = 0;
    v10 = nullptr;
    v7 = nullptr;
  }
  v60 = (_QWORD **)v7;
  sub_1407C9510(&v55);
  v31 = (__int64)v10 - v6;
  v32 = ((__int64)v10 - v6) >> 3;
  v33 = v55;
  if ( (__int64)(v57 - v55) >> 3 < v32 )
  {
    if ( v31 < 0 )
      sub_1400526C0(v30);
    v34 = v56;
    v35 = sub_1407E4490(qword_141ABD470, v31);
    sub_141758A00();
    if ( v55 == 0 )
      goto LABEL_66;
    v36 = v57 - v55;
    if ( v57 - v55 == -1 )
    {
      v36 = *(unsigned int *)(v55 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_65;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_65;
    }
    v37 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v37) >> 3 > v36 )
    {
      v38 = *(_QWORD *)(v37 + 8 * v36);
      if ( v38 != 0 )
      {
        v54 = v38;
        MEMORY[0x1419475D8](v38 + 32, v55 - *(unsigned int *)(v38 + 120));
        v30 = v54;
        if ( (*(_BYTE *)(v54 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v54 + 64)) == 0)
          && *(_BYTE *)(v54 + 97) != 0 )
        {
          sub_1412D33C0(v54);
        }
        goto LABEL_66;
      }
    }
LABEL_65:
    MEMORY[0x141948990](v55 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_66:
    v55 = v35;
    v56 = v35 + v34 - v33;
    v57 = v35 + 8 * v32;
  }
  if ( v10 != (_QWORD *)v6 )
  {
    v39 = 1;
    if ( v32 >= 2 )
      v39 = ((__int64)v10 - v6) >> 3;
    v40 = 0;
    do
    {
      v41 = *(_QWORD *)(v6 + 8 * v40);
      if ( v41 != 0 )
      {
        v42 = sub_14083D4F0(v30);
        v59 = 0;
        v58 = v42 + 8;
        sub_140EAA560(v41, &v58);
        sub_14083B5F0(&v55, &v58);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v58 + 16LL))(v58, &v58);
      }
      ++v40;
    }
    while ( v39 != v40 );
  }
  sub_14083DB80(&v58, &v55);
  v43 = *v53;
  if ( &v58 == v53 )
  {
    v44 = v60;
  }
  else
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v43 + 16LL))(v43, v53);
    v44 = v60;
    v45 = v58;
    v46 = v59;
    v53[1] = v59;
    *v53 = v45;
    v43 = sub_14083D4F0(v46) + 8;
    v59 = 0;
    v58 = v43;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v43 + 16LL))(v43, &v58);
  result = sub_14083B0A0(&v55);
  if ( v10 != (_QWORD *)v6 )
  {
    v48 = (_QWORD *)v6;
    do
    {
      if ( *v48 != 0 )
        result = sub_141750CFC(*v48);
      ++v48;
    }
    while ( v48 != v10 );
  }
  if ( v6 != 0 )
  {
    v49 = (unsigned __int64)v44 - v6;
    if ( v49 == -1 )
    {
      v49 = *(unsigned int *)(v6 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v50 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v50) >> 3 <= v49 )
      return MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
    v51 = *(_QWORD *)(v50 + 8 * v49);
    if ( v51 == 0 )
      return MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v51 + 32, v6 - *(unsigned int *)(v51 + 120));
    if ( *(_BYTE *)(v51 + 72) != 0 )
    {
      v52 = _InterlockedDecrement((volatile signed __int32 *)(v51 + 64));
      result = v52 != 0;
      if ( v52 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v51 + 97) != 0 )
      return sub_1412D33C0(v51);
  }
  return result;
}
