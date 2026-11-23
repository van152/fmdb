char __fastcall sub_14101DBD0(_QWORD *a1, _QWORD *a2, __int64 a3, int a4, char a5, char a6, char a7)
{
  _QWORD *v9; // r14
  _QWORD *v11; // rax
  _QWORD *v12; // rax
  unsigned __int8 v13; // bl
  unsigned int v14; // eax
  int v15; // ecx
  void *v17; // rcx
  __int64 v18; // rdi
  __int64 v19; // rsi
  __int64 v20; // rdi
  __int64 v21; // rax
  __int64 v22; // rcx
  unsigned __int64 i; // rdi
  __int64 v24; // rsi
  char v25; // bl
  __int64 v26; // r12
  __int64 *v27; // rbx
  __int64 v28; // r15
  unsigned __int64 v29; // rax
  unsigned __int64 v30; // rsi
  unsigned __int64 v31; // rdx
  unsigned __int64 v32; // rsi
  __int64 v33; // rax
  __int64 v34; // r12
  __int64 *v35; // rdi
  __int64 v36; // rdi
  unsigned __int64 v37; // rcx
  __int64 v38; // rbx
  __int64 v39; // rbx
  bool v40; // al
  __int64 v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rcx
  __int64 v44; // rax
  unsigned __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rsi
  bool v48; // al
  __int64 v49; // [rsp+48h] [rbp-38h] BYREF
  __int64 v50; // [rsp+50h] [rbp-30h] BYREF
  __int128 v51; // [rsp+60h] [rbp-20h] BYREF
  __int64 v52; // [rsp+70h] [rbp-10h]
  __int64 v53; // [rsp+78h] [rbp-8h] BYREF
  int v54; // [rsp+80h] [rbp+0h]
  unsigned __int64 v55; // [rsp+88h] [rbp+8h]
  __int64 v56; // [rsp+90h] [rbp+10h]

  v56 = -2;
  if ( a2 == nullptr )
    return 0;
  v9 = a2;
  if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a2 + 56LL))(a2) == 3 )
  {
    v11 = (_QWORD *)v9[3];
    if ( v11 == (_QWORD *)v9[4] )
      goto LABEL_8;
    v12 = (_QWORD *)*v11;
    if ( v12 == nullptr )
      goto LABEL_8;
  }
  else
  {
    v12 = v9;
  }
  v9 = v12;
LABEL_8:
  v13 = sub_14101D650(a1, v9);
  if ( (unsigned __int8)sub_14101D990(a1, v9) == 0 )
    goto LABEL_15;
  v14 = (*(__int64 (__fastcall **)(_QWORD *))(*v9 + 56LL))(v9);
  if ( v14 > 0x19 )
    goto LABEL_15;
  v15 = 50332201;
  if ( !_bittest(&v15, v14) )
  {
    if ( v14 == 1 && (*(unsigned int (__fastcall **)(_QWORD *))(*v9 + 56LL))(v9) == 1 )
    {
      if ( (((*(__int64 (__fastcall **)(_QWORD *))(*v9 + 1760LL))(v9) == 0) | v13) == 0 )
        return 0;
    }
    else
    {
LABEL_15:
      if ( v13 == 0 )
        return 0;
    }
  }
  v17 = (void *)qword_141ABD470;
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
    v17 = &unk_141B59A68;
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v51 = 0;
  v52 = 0;
  if ( a3 != 0 && &v51 != (__int128 *)a3 )
  {
    v18 = (__int64)(*(_QWORD *)(a3 + 8) - *(_QWORD *)a3) >> 2;
    v19 = *(_QWORD *)(a3 + 8) - *(_QWORD *)a3;
    if ( v19 != 0 )
    {
      if ( v19 < 0 )
        sub_1400526C0(v17);
      *(_QWORD *)&v51 = sub_1407E4490(v17, v19);
      *((_QWORD *)&v51 + 1) = v51;
      v20 = v51 + 4 * v18;
      v52 = v20;
      sub_141758A00();
    }
    else
    {
      v20 = 4 * v18;
      sub_1417589F0();
    }
    *((_QWORD *)&v51 + 1) = v20;
  }
  LODWORD(v55) = a4;
  v21 = a1[54];
  v22 = a1[55];
  if ( v22 != v21 )
  {
    for ( i = 0; i < (v22 - v21) >> 3; ++i )
    {
      v24 = *(_QWORD *)(v21 + 8 * i);
      if ( v24 != 0 )
      {
        (*(void (__fastcall **)(_QWORD *, __int64 *))(*v9 + 144LL))(v9, &v49);
        v25 = sub_140FEB670(v24, (__int64)&v49);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v50 + 16LL))(v50, &v50);
        if ( v25 != 0 )
        {
          sub_14150FC30(v24, (_DWORD)a1, (unsigned int)&v51, v55, a5, a7, 0);
          goto LABEL_51;
        }
        v21 = a1[54];
        v22 = a1[55];
      }
    }
  }
  v26 = sub_141750CC0(88);
  sub_14150F9A0(v26, (_DWORD)a1, (_DWORD)v9, (unsigned int)&v51, v55, a5, a7, a6);
  v27 = (__int64 *)a1[55];
  if ( v27 == (__int64 *)a1[56] )
  {
    v28 = (__int64)v27 - a1[54];
    v29 = v28 >> 3;
    v30 = (unsigned __int64)(v28 >> 3) >> 1;
    v31 = 0x1FFFFFFFFFFFFFFFLL - v30;
    v32 = (v28 >> 3) + v30;
    v55 = (v28 >> 3) + 1;
    if ( v32 <= v55 )
      v32 = v29 + 1;
    if ( v29 > v31 )
      v32 = 0x1FFFFFFFFFFFFFFFLL;
    v33 = sub_1407E4490(qword_141ABD470, 8 * v32);
    *(_QWORD *)(v33 + v28) = v26;
    v34 = v33;
    v35 = (__int64 *)a1[55];
    sub_141758A00();
    if ( v35 != v27 )
      sub_141758A00();
    v36 = a1[54];
    if ( v36 != 0 )
    {
      v37 = a1[56] - v36;
      if ( v37 == -1 )
        v37 = *(unsigned int *)(v36 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v38 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v38) >> 3 > v37)
        && (v39 = *(_QWORD *)(v38 + 8 * v37)) != 0 )
      {
        MEMORY[0x1419475D8](v39 + 32, v36 - *(unsigned int *)(v39 + 120));
        v40 = *(_BYTE *)(v39 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 + 64)) != 0;
        if ( !v40 && *(_BYTE *)(v39 + 97) != 0 )
          sub_1412D33C0(v39);
      }
      else
      {
        MEMORY[0x141948990](v36 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    a1[54] = v34;
    a1[55] = v34 + 8 * v55;
    a1[56] = v34 + 8 * v32;
  }
  else
  {
    *v27 = v26;
    a1[55] += 8LL;
  }
LABEL_51:
  sub_1407C9510(&v49);
  v42 = sub_14083D4F0(v41);
  v54 = 1853059955;
  v53 = v42 + 56;
  sub_14083B5F0(&v49, &v53);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v53 + 16LL))(v53, &v53);
  v44 = sub_14083D4F0(v43);
  v54 = 1935829358;
  v53 = v44 + 56;
  sub_14083B5F0(&v49, &v53);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v53 + 16LL))(v53, &v53);
  (*(void (__fastcall **)(__int64, _QWORD *, _QWORD *, __int64 *))(*(_QWORD *)qword_141B5EF38 + 56LL))(
    qword_141B5EF38,
    a1,
    v9,
    &v49);
  sub_14083B0A0(&v49);
  if ( (_QWORD)v51 == 0 )
    return 1;
  v45 = v52 - v51;
  if ( v52 - (_QWORD)v51 == -1 )
  {
    v45 = *(unsigned int *)(v51 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      goto LABEL_60;
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    goto LABEL_60;
  }
  v46 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v46) >> 3 > v45 )
  {
    v47 = *(_QWORD *)(v46 + 8 * v45);
    if ( v47 != 0 )
    {
      MEMORY[0x1419475D8](v47 + 32, v51 - *(unsigned int *)(v47 + 120));
      v48 = *(_BYTE *)(v47 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v47 + 64)) != 0;
      if ( !v48 && *(_BYTE *)(v47 + 97) != 0 )
        sub_1412D33C0(v47);
      return 1;
    }
  }
LABEL_60:
  MEMORY[0x141948990](v51 - *(unsigned int *)(qword_141ABD470 + 48));
  return 1;
}
