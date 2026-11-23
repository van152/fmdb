char __fastcall sub_140E96790(_QWORD *a1, __int64 *a2)
{
  __int64 v2; // rsi
  __int64 v4; // r12
  __int64 v5; // r14
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rcx
  __int64 v9; // rdx
  unsigned __int64 v10; // rsi
  __int64 v11; // r15
  __int64 v12; // r13
  __int64 v13; // r14
  unsigned __int64 v14; // rcx
  __int64 v15; // r8
  __int64 v16; // rcx
  __int64 v17; // rbx
  __int64 i; // rdi
  __int64 v19; // rsi
  __int64 v20; // rax
  __int64 v21; // rcx
  __int64 v22; // rax
  __int64 v23; // rcx
  char result; // al
  unsigned __int64 v25; // r14
  __int64 v26; // rcx
  __int64 v27; // rdi
  signed __int32 v28; // et0
  __int64 v30; // [rsp+28h] [rbp-38h]
  __int64 v31; // [rsp+30h] [rbp-30h]
  __int64 v32; // [rsp+38h] [rbp-28h] BYREF
  __int64 v33; // [rsp+40h] [rbp-20h]
  unsigned __int64 v34; // [rsp+48h] [rbp-18h]
  __int64 v35; // [rsp+50h] [rbp-10h] BYREF
  __int64 v36; // [rsp+58h] [rbp-8h]
  __int64 v37; // [rsp+60h] [rbp+0h]

  v37 = -2;
  v2 = a1[1] - *a1;
  if ( v2 != 0 )
  {
    if ( v2 < 0 )
      sub_1400526C0(a1);
    v4 = sub_1407E4490(qword_141ABD470, v2);
    v5 = v4 + 8 * (v2 >> 3);
    v6 = a1[1] - *a1;
    sub_141758A00();
    v7 = v4 + v6;
  }
  else
  {
    v4 = 0;
    v7 = 0;
    v5 = 0;
  }
  sub_1407C9510(&v32);
  v9 = v7 - v4;
  v10 = (v7 - v4) >> 3;
  v11 = v32;
  if ( (__int64)(v34 - v32) >> 3 < v10 )
  {
    v30 = v5;
    if ( v9 < 0 )
      sub_1400526C0(v8);
    v12 = v33;
    v13 = sub_1407E4490(qword_141ABD470, v9);
    sub_141758A00();
    if ( v32 == 0 )
      goto LABEL_18;
    v14 = v34 - v32;
    if ( v34 - v32 == -1 )
    {
      v14 = *(unsigned int *)(v32 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_17;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_17;
    }
    v15 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v15) >> 3 > v14 )
    {
      v16 = *(_QWORD *)(v15 + 8 * v14);
      if ( v16 != 0 )
      {
        v31 = v16;
        MEMORY[0x1419475D8](v16 + 32, v32 - *(unsigned int *)(v16 + 120));
        v8 = v31;
        if ( (*(_BYTE *)(v31 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) == 0)
          && *(_BYTE *)(v31 + 97) != 0 )
        {
          sub_1412D33C0(v31);
        }
        goto LABEL_18;
      }
    }
LABEL_17:
    MEMORY[0x141948990](v32 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_18:
    v32 = v13;
    v33 = v13 + v12 - v11;
    v34 = v13 + 8 * v10;
    v5 = v30;
  }
  if ( v7 != v4 )
  {
    v17 = 1;
    if ( v10 >= 2 )
      v17 = v10;
    for ( i = 0; i != v17; ++i )
    {
      v19 = *(_QWORD *)(v4 + 8 * i);
      if ( v19 != 0 )
      {
        v20 = sub_14083D4F0(v8);
        v36 = 0;
        v35 = v20 + 8;
        sub_140EB2070(v19, &v35);
        sub_14083B5F0(&v32, &v35);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v35 + 16LL))(v35, &v35);
      }
    }
  }
  sub_14083DB80(&v35, &v32);
  v21 = *a2;
  if ( &v35 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, a2);
    v22 = v35;
    v23 = v36;
    a2[1] = v36;
    *a2 = v22;
    v21 = sub_14083D4F0(v23) + 8;
    v36 = 0;
    v35 = v21;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v21 + 16LL))(v21, &v35);
  result = sub_14083B0A0(&v32);
  if ( v4 != 0 )
  {
    v25 = v5 - v4;
    if ( v25 == -1 )
    {
      v25 = *(unsigned int *)(v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v26 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 <= v25 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    v27 = *(_QWORD *)(v26 + 8 * v25);
    if ( v27 == 0 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v27 + 32, v4 - *(unsigned int *)(v27 + 120));
    if ( *(_BYTE *)(v27 + 72) != 0 )
    {
      v28 = _InterlockedDecrement((volatile signed __int32 *)(v27 + 64));
      result = v28 != 0;
      if ( v28 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v27 + 97) != 0 )
      return sub_1412D33C0(v27);
  }
  return result;
}
