char __fastcall sub_140E96CA0(__int64 a1, __int64 *a2)
{
  __int64 v4; // rcx
  _QWORD **v5; // r13
  _QWORD **v6; // r14
  __int64 v7; // rdx
  __int64 v8; // r15
  unsigned __int64 v9; // rcx
  __int64 v10; // rdi
  __int64 v11; // rsi
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  __int64 v15; // r15
  __int64 *v16; // r12
  _QWORD *v17; // rdi
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 v20; // rax
  __int64 *v21; // r13
  __int64 v22; // r12
  __int64 v23; // rbx
  unsigned __int64 v24; // r14
  __int64 i; // rbx
  __int64 *v26; // rdx
  unsigned int v27; // r12d
  __int64 v28; // rcx
  __int64 v29; // rax
  __int64 v30; // rax
  __int64 v31; // rcx
  __int64 v32; // rax
  __int64 v33; // rcx
  char result; // al
  _QWORD **v35; // rbx
  _QWORD **v36; // rsi
  _QWORD *v37; // rdi
  unsigned __int64 v38; // rcx
  __int64 v39; // rdx
  __int64 v40; // rdi
  signed __int32 v41; // et0
  __int64 v42; // [rsp+28h] [rbp-58h] BYREF
  int v43; // [rsp+30h] [rbp-50h]
  __int64 v44; // [rsp+38h] [rbp-48h]
  _QWORD **v45; // [rsp+40h] [rbp-40h]
  __int64 *v46; // [rsp+48h] [rbp-38h]
  __int128 v47; // [rsp+50h] [rbp-30h] BYREF
  __int64 v48; // [rsp+60h] [rbp-20h]
  __int64 v49; // [rsp+68h] [rbp-18h]
  __int64 v50; // [rsp+70h] [rbp-10h]
  char v51; // [rsp+78h] [rbp-8h]
  unsigned __int64 v52; // [rsp+88h] [rbp+8h]
  __int64 v53; // [rsp+90h] [rbp+10h] BYREF
  __int64 v54; // [rsp+98h] [rbp+18h]
  __int64 v55; // [rsp+A0h] [rbp+20h] BYREF
  __int64 v56; // [rsp+A8h] [rbp+28h]
  __int64 v57; // [rsp+B8h] [rbp+38h] BYREF
  __int64 v58; // [rsp+C0h] [rbp+40h]
  __int64 v59; // [rsp+C8h] [rbp+48h] BYREF
  __int64 v60; // [rsp+D0h] [rbp+50h]
  __int64 v61; // [rsp+D8h] [rbp+58h]
  __int64 v62; // [rsp+E0h] [rbp+60h]

  v62 = -2;
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
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v47 = 0;
  v48 = 0;
  sub_140EB4350(&v47, a1);
  v51 = *(_BYTE *)(a1 + 40);
  v4 = *(_QWORD *)(a1 + 24);
  v50 = *(_QWORD *)(a1 + 32);
  v49 = v4;
  sub_140FE8760(v4);
  sub_1407C9510(&v59);
  v5 = *((_QWORD ***)&v47 + 1);
  v6 = (_QWORD **)v47;
  v7 = *((_QWORD *)&v47 + 1) - v47;
  v8 = v59;
  v9 = (__int64)(*((_QWORD *)&v47 + 1) - v47) >> 3;
  v52 = v9;
  if ( (v61 - v59) >> 3 >= v9 )
  {
    if ( *((_QWORD *)&v47 + 1) == (_QWORD)v47 )
      goto LABEL_37;
    goto LABEL_20;
  }
  if ( v7 < 0 )
    sub_1400526C0(v9);
  v10 = v60;
  v11 = sub_1407E4490(qword_141ABD470, v7);
  sub_141758A00();
  if ( v59 != 0 )
  {
    v12 = v61 - v59;
    if ( v61 - v59 == -1 )
    {
      v12 = *(unsigned int *)(v59 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_18:
        MEMORY[0x141948990](v59 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_19;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_18;
    }
    v13 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12 )
    {
      v14 = *(_QWORD *)(v13 + 8 * v12);
      if ( v14 != 0 )
      {
        MEMORY[0x1419475D8](v14 + 32, v59 - *(unsigned int *)(v14 + 120));
        if ( (*(_BYTE *)(v14 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) == 0)
          && *(_BYTE *)(v14 + 97) != 0 )
        {
          sub_1412D33C0(v14);
        }
        goto LABEL_19;
      }
    }
    goto LABEL_18;
  }
LABEL_19:
  v59 = v11;
  v60 = v11 + v10 - v8;
  v61 = v11 + 8 * v52;
  v6 = (_QWORD **)v47;
LABEL_20:
  v46 = a2;
  v15 = 0;
  v16 = &v42;
  v45 = v6;
  do
  {
    v17 = v6[v15];
    if ( v17 != nullptr )
    {
      v18 = sub_14083D4F0(v9);
      v54 = 0;
      v53 = v18 + 8;
      sub_1407C9510(&v55);
      sub_141526230(&v55);
      v20 = sub_14083D4F0(v19);
      v43 = 1668048498;
      v42 = v20 + 56;
      sub_14083B5F0(&v55, v16);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v42 + 16LL))(v42, v16);
      v21 = v16;
      sub_1407C9510(v16);
      v22 = v55;
      v23 = v56;
      v24 = (v56 - v55) >> 3;
      if ( (v44 - v42) >> 4 < v24 )
      {
        if ( (unsigned __int64)(v56 - v55) >= 0x7FFFFFFFFFFFFFF9LL )
          sub_1400526C0(0x7FFFFFFFFFFFFFF9LL);
        sub_140837DD0(v21, (v56 - v55) >> 3);
      }
      if ( v23 != v22 )
      {
        if ( v24 < 2 )
          v24 = 1;
        for ( i = 0; i != v24; ++i )
        {
          v26 = *(__int64 **)(v55 + 8 * i);
          if ( v26 == nullptr )
            v26 = &qword_141B5A4A0;
          v27 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v26 + 80LL))(*v26);
          v29 = sub_14083D4F0(v28);
          v58 = 0;
          v57 = v29 + 8;
          if ( (unsigned __int8)sub_1415332F0(v17, v27, &v57) != 0 )
            sub_140835380(v21, v27, &v57);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v57 + 16LL))(v57, &v57);
        }
      }
      v16 = v21;
      sub_14083DDA0(&v57, v21);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v53 + 16LL))(v53, &v53);
      v54 = v58;
      v53 = v57;
      v30 = sub_14083D4F0(v58);
      v58 = 0;
      v57 = v30 + 8;
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)(v30 + 8) + 16LL))(v30 + 8, &v57);
      v6 = v45;
      sub_140833970(v21);
      sub_14083B0A0(&v55);
      sub_14083B5F0(&v59, &v53);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v53 + 16LL))(v53, &v53);
    }
    ++v15;
  }
  while ( v15 != v52 );
  v5 = v6;
  a2 = v46;
LABEL_37:
  sub_14083DB80(&v55, &v59);
  v31 = *a2;
  if ( &v55 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, a2);
    v32 = v55;
    v33 = v56;
    a2[1] = v56;
    *a2 = v32;
    v31 = sub_14083D4F0(v33) + 8;
    v56 = 0;
    v55 = v31;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, &v55);
  result = sub_14083B0A0(&v59);
  v35 = *((_QWORD ***)&v47 + 1);
  if ( v5 != *((_QWORD ***)&v47 + 1) )
  {
    v36 = v5;
    do
    {
      v37 = *v36;
      if ( *v36 != nullptr )
      {
        if ( *v37 != 0 )
          sub_140FB3720();
        result = sub_141750CFC(v37);
      }
      ++v36;
    }
    while ( v36 != v35 );
    *((_QWORD *)&v47 + 1) = v5;
  }
  if ( v5 != nullptr )
  {
    v38 = v48 - (_QWORD)v5;
    if ( v48 - (_QWORD)v5 == -1 )
    {
      v38 = *(unsigned int *)((char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990]((char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990]((char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v39 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v39) >> 3 <= v38 )
      return MEMORY[0x141948990]((char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
    v40 = *(_QWORD *)(v39 + 8 * v38);
    if ( v40 == 0 )
      return MEMORY[0x141948990]((char *)v5 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v40 + 32, (char *)v5 - *(unsigned int *)(v40 + 120));
    if ( *(_BYTE *)(v40 + 72) != 0 )
    {
      v41 = _InterlockedDecrement((volatile signed __int32 *)(v40 + 64));
      result = v41 != 0;
      if ( v41 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v40 + 97) != 0 )
      return sub_1412D33C0(v40);
  }
  return result;
}
