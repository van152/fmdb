char __fastcall sub_140E96120(__int64 a1, __int64 *a2)
{
  __int64 v3; // r12
  unsigned __int64 v4; // r14
  unsigned __int64 v5; // rdi
  unsigned __int64 v6; // rcx
  bool v7; // cf
  unsigned __int64 v8; // rcx
  __int64 v9; // r13
  unsigned __int64 v10; // rcx
  __int64 v11; // rsi
  __int64 v12; // r14
  unsigned __int64 v13; // rcx
  __int64 v14; // rcx
  __int64 v15; // rax
  __int64 v16; // rcx
  char result; // al
  _QWORD **v18; // rbx
  __int64 v19; // r14
  _QWORD **v20; // rsi
  _QWORD *v21; // rdi
  unsigned __int64 v22; // rcx
  __int64 v23; // rdx
  __int64 v24; // rdi
  signed __int32 v25; // et0
  __int64 v26; // r8
  __int64 v27; // r15
  __int64 v28; // rsi
  __int64 v29; // rax
  __int128 v31; // [rsp+30h] [rbp-50h] BYREF
  __int64 v32; // [rsp+40h] [rbp-40h]
  __int64 v33; // [rsp+48h] [rbp-38h]
  unsigned __int64 v34; // [rsp+50h] [rbp-30h]
  char v35; // [rsp+58h] [rbp-28h]
  __int64 v36; // [rsp+68h] [rbp-18h] BYREF
  __int64 v37; // [rsp+70h] [rbp-10h]
  __int64 v38; // [rsp+78h] [rbp-8h]
  __int64 v39; // [rsp+80h] [rbp+0h] BYREF
  __int64 v40; // [rsp+88h] [rbp+8h]
  __int64 v41; // [rsp+90h] [rbp+10h]

  v41 = -2;
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
  v31 = 0;
  v32 = 0;
  sub_140EB4350(&v31, a1);
  v35 = *(_BYTE *)(a1 + 40);
  v3 = *(_QWORD *)(a1 + 24);
  v34 = *(_QWORD *)(a1 + 32);
  v33 = v3;
  sub_140FE8760(v3);
  sub_1407C9510(&v36);
  v4 = v34;
  v5 = 0;
  v6 = (__int64)(*(_QWORD *)(v3 + 288) - *(_QWORD *)(v3 + 280)) >> 3;
  v7 = v6 < v34;
  v8 = v6 - v34;
  if ( !v7 )
    v5 = v8;
  v9 = v36;
  v10 = (v38 - v36) >> 3;
  if ( v10 >= v5 )
  {
    if ( (__int64)(*(_QWORD *)(v3 + 288) - *(_QWORD *)(v3 + 280)) >> 3 <= v34 )
      goto LABEL_13;
    goto LABEL_46;
  }
  if ( v5 >> 61 != 0 )
    sub_1400526C0(v10);
  v11 = v37;
  v12 = sub_1407E4490(qword_141ABD470, 8 * v5);
  sub_141758A00();
  if ( v36 != 0 )
  {
    v13 = v38 - v36;
    if ( v38 - v36 == -1 )
    {
      v13 = *(unsigned int *)(v36 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_42:
        MEMORY[0x141948990](v36 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_43;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_42;
    }
    v26 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > v13 )
    {
      v27 = *(_QWORD *)(v26 + 8 * v13);
      if ( v27 != 0 )
      {
        MEMORY[0x1419475D8](v27 + 32, v36 - *(unsigned int *)(v27 + 120));
        if ( (*(_BYTE *)(v27 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) == 0)
          && *(_BYTE *)(v27 + 97) != 0 )
        {
          sub_1412D33C0(v27);
        }
        goto LABEL_43;
      }
    }
    goto LABEL_42;
  }
LABEL_43:
  v36 = v12;
  v37 = v12 + v11 - v9;
  v38 = v12 + 8 * v5;
  v3 = v33;
  v4 = v34;
  do
  {
LABEL_46:
    v28 = *(_QWORD *)(*(_QWORD *)(v3 + 280) + 8 * v4);
    if ( v28 != 0 )
    {
      v29 = sub_14083D4F0(v10);
      v40 = 0;
      v39 = v29 + 8;
      sub_140EAF580(v28, &v39);
      sub_14083B5F0(&v36, &v39);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v39 + 16LL))(v39, &v39);
    }
    ++v4;
    --v5;
  }
  while ( v5 != 0 );
LABEL_13:
  sub_14083DB80(&v39, &v36);
  v14 = *a2;
  if ( &v39 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, a2);
    v15 = v39;
    v16 = v40;
    a2[1] = v40;
    *a2 = v15;
    v14 = sub_14083D4F0(v16) + 8;
    v40 = 0;
    v39 = v14;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v39);
  result = sub_14083B0A0(&v36);
  v18 = *((_QWORD ***)&v31 + 1);
  v19 = v31;
  if ( (_QWORD)v31 == *((_QWORD *)&v31 + 1) )
  {
    v19 = *((_QWORD *)&v31 + 1);
    if ( *((_QWORD *)&v31 + 1) == 0 )
      return result;
  }
  else
  {
    v20 = (_QWORD **)v31;
    do
    {
      v21 = *v20;
      if ( *v20 != nullptr )
      {
        if ( *v21 != 0 )
          sub_140FB3720();
        result = sub_141750CFC(v21);
      }
      ++v20;
    }
    while ( v20 != v18 );
    *((_QWORD *)&v31 + 1) = v19;
    if ( v19 == 0 )
      return result;
  }
  v22 = v32 - v19;
  if ( v32 - v19 == -1 )
  {
    v22 = *(unsigned int *)(v19 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      return MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    return MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
  }
  v23 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v23) >> 3 <= v22 )
    return MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
  v24 = *(_QWORD *)(v23 + 8 * v22);
  if ( v24 == 0 )
    return MEMORY[0x141948990](v19 - *(unsigned int *)(qword_141ABD470 + 48));
  MEMORY[0x1419475D8](v24 + 32, v19 - *(unsigned int *)(v24 + 120));
  if ( *(_BYTE *)(v24 + 72) != 0 )
  {
    v25 = _InterlockedDecrement((volatile signed __int32 *)(v24 + 64));
    result = v25 != 0;
    if ( v25 != 0 )
      return result;
  }
  else
  {
    result = 0;
  }
  if ( *(_BYTE *)(v24 + 97) != 0 )
    return sub_1412D33C0(v24);
  return result;
}
