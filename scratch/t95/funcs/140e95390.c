char __fastcall sub_140E95390(_QWORD *a1, __int64 *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rcx
  __int128 v7; // kr00_16
  __int64 v8; // rdx
  unsigned __int64 v9; // rbx
  __int64 v10; // r13
  __int64 v11; // r15
  __int64 v12; // rdi
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // rcx
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int128 *v18; // rbx
  __int64 i; // r14
  __int64 v20; // rdi
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // rcx
  char result; // al
  unsigned __int64 v26; // rcx
  __int64 v27; // rbx
  __int64 v28; // rsi
  signed __int32 v29; // et0
  __int64 *v30; // [rsp+28h] [rbp-58h]
  __int128 v31; // [rsp+30h] [rbp-50h] BYREF
  __int64 v32; // [rsp+40h] [rbp-40h]
  __int64 v33; // [rsp+48h] [rbp-38h]
  __int128 *v34; // [rsp+58h] [rbp-28h] BYREF
  __int64 v35; // [rsp+60h] [rbp-20h]
  __int64 v36; // [rsp+68h] [rbp-18h] BYREF
  __int64 v37; // [rsp+70h] [rbp-10h]
  unsigned __int64 v38; // [rsp+78h] [rbp-8h]
  __int64 v39; // [rsp+80h] [rbp+0h] BYREF
  __int64 v40; // [rsp+88h] [rbp+8h]
  __int64 v41; // [rsp+90h] [rbp+10h]

  v41 = -2;
  v31 = 0;
  v32 = 0;
  v4 = a1[1] - *a1;
  if ( v4 != 0 )
  {
    if ( v4 < 0 )
      sub_1400526C0(a1);
    *(_QWORD *)&v31 = sub_1407E4490(qword_141ABD470, v4);
    v32 = v31 + 8 * (v4 >> 3);
    v5 = a1[1] - *a1;
    sub_141758A00();
    *((_QWORD *)&v31 + 1) = v31 + v5;
  }
  v30 = a2;
  v33 = a1[3];
  v34 = &v31;
  sub_1407C9510(&v36);
  v7 = v31;
  v8 = *((_QWORD *)&v31 + 1) - v31;
  v9 = (__int64)(*((_QWORD *)&v31 + 1) - v31) >> 3;
  v10 = v36;
  if ( (__int64)(v38 - v36) >> 3 < v9 )
  {
    if ( v8 < 0 )
      sub_1400526C0(v6);
    v11 = v37;
    v12 = sub_1407E4490(qword_141ABD470, v8);
    sub_141758A00();
    if ( v36 == 0 )
      goto LABEL_17;
    v13 = v38 - v36;
    if ( v38 - v36 == -1 )
    {
      v13 = *(unsigned int *)(v36 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_16;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_16;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v13);
      if ( v15 != 0 )
      {
        v16 = v36 - *(unsigned int *)(v15 + 120);
        v35 = v15;
        MEMORY[0x1419475D8](v15 + 32, v16);
        v6 = v35;
        if ( (*(_BYTE *)(v35 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v35 + 64)) == 0)
          && *(_BYTE *)(v6 + 97) != 0 )
        {
          sub_1412D33C0(v6);
        }
        goto LABEL_17;
      }
    }
LABEL_16:
    MEMORY[0x141948990](v36 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_17:
    v36 = v12;
    v37 = v12 + v11 - v10;
    v38 = v12 + 8 * v9;
  }
  if ( *((_QWORD *)&v7 + 1) != (_QWORD)v7 )
  {
    v17 = 1;
    if ( v9 >= 2 )
      v17 = v9;
    v18 = v34;
    for ( i = 0; i != v17; ++i )
    {
      v20 = *(_QWORD *)(*(_QWORD *)v18 + 8 * i);
      if ( v20 != 0 )
      {
        v21 = sub_14083D4F0(v6);
        v40 = 0;
        v39 = v21 + 8;
        sub_140DF4BA0(&v34, v20, &v39);
        sub_14083B5F0(&v36, &v39);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v39 + 16LL))(v39, &v39);
      }
    }
  }
  sub_14083DB80(&v39, &v36);
  v22 = *v30;
  if ( &v39 != v30 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, v30);
    v23 = v39;
    v24 = v40;
    v30[1] = v40;
    *v30 = v23;
    v22 = sub_14083D4F0(v24) + 8;
    v40 = 0;
    v39 = v22;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v39);
  result = sub_14083B0A0(&v36);
  if ( (_QWORD)v31 != 0 )
  {
    v26 = v32 - v31;
    if ( v32 - (_QWORD)v31 == -1 )
    {
      v26 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v27 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v27) >> 3 <= v26 )
      return MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
    v28 = *(_QWORD *)(v27 + 8 * v26);
    if ( v28 == 0 )
      return MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v28 + 32, v31 - *(unsigned int *)(v28 + 120));
    if ( *(_BYTE *)(v28 + 72) != 0 )
    {
      v29 = _InterlockedDecrement((volatile signed __int32 *)(v28 + 64));
      result = v29 != 0;
      if ( v29 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v28 + 97) != 0 )
      return sub_1412D33C0(v28);
  }
  return result;
}
