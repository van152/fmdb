// THUNK ALIAS -> sub_143EE11B0 (jmp:0x14104f9b0->0x143ee11b0)
__int64 __fastcall sub_143EE11B0(__int64 ***a1, __int64 *a2)
{
  __int64 *v4; // rcx
  __int64 *v5; // rdx
  __int64 *v6; // rbx
  __int64 *v7; // rdi
  __int64 *v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rdx
  unsigned __int64 v12; // rdi
  __int64 v13; // r13
  __int64 v14; // rsi
  __int64 v15; // r14
  unsigned __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 v21; // r8
  __int64 v22; // r15
  __int64 v23; // rbx
  __int64 v24; // rcx
  __int64 v25; // rsi
  __int64 v26; // rax
  __int64 *v27; // [rsp+20h] [rbp-30h]
  __int64 v28; // [rsp+28h] [rbp-28h] BYREF
  __int64 v29; // [rsp+30h] [rbp-20h]
  unsigned __int64 v30; // [rsp+38h] [rbp-18h]
  __int64 v31; // [rsp+40h] [rbp-10h] BYREF
  __int64 v32; // [rsp+48h] [rbp-8h]
  __int64 v33; // [rsp+50h] [rbp+0h]

  v33 = -2;
  sub_1407C9510(&v28);
  v4 = **a1;
  v5 = v4 + 19;
  v6 = v4 + 22;
  v7 = v4 + 18;
  v8 = v4 + 21;
  if ( *((_BYTE *)*a1 + 8) == 0 )
    v5 = v6;
  v9 = *v5;
  if ( *((_BYTE *)*a1 + 8) != 0 )
    v8 = v7;
  v10 = *v8;
  v11 = v9 - v10;
  v12 = (v9 - v10) >> 3;
  v13 = v28;
  v27 = a2;
  if ( (__int64)(v30 - v28) >> 3 >= v12 )
  {
    if ( v9 == v10 )
      goto LABEL_12;
    goto LABEL_23;
  }
  if ( v11 < 0 )
    sub_1400526C0(v10);
  v14 = v29;
  v15 = sub_1407E4490(qword_141ABD470, v11);
  sub_141758A00();
  if ( v28 != 0 )
  {
    v16 = v30 - v28;
    if ( v30 - v28 == -1 )
    {
      v16 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_21:
        MEMORY[0x141948990](v28 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_22;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_21;
    }
    v21 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v16 )
    {
      v22 = *(_QWORD *)(v21 + 8 * v16);
      if ( v22 != 0 )
      {
        MEMORY[0x1419475D8](v22 + 32, v28 - *(unsigned int *)(v22 + 120));
        if ( (*(_BYTE *)(v22 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) == 0)
          && *(_BYTE *)(v22 + 97) != 0 )
        {
          sub_1412D33C0(v22);
        }
        goto LABEL_22;
      }
    }
    goto LABEL_21;
  }
LABEL_22:
  v28 = v15;
  v29 = v15 + v14 - v13;
  v30 = v15 + 8 * v12;
LABEL_23:
  v23 = 0;
  do
  {
    v24 = 18;
    if ( *((_BYTE *)*a1 + 8) == 0 )
      v24 = 21;
    v25 = *(_QWORD *)((**a1)[v24] + (v23 >> 29));
    if ( v25 != 0 )
    {
      v26 = sub_14083D4F0(v23 >> 29);
      v32 = 0;
      v31 = v26 + 8;
      sub_14104FCD0(v25, &v31);
      sub_14083B5F0(&v28, &v31);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, &v31);
    }
    v23 += 0x100000000LL;
    --v12;
  }
  while ( v12 != 0 );
LABEL_12:
  sub_14083DB80(&v31, &v28);
  v17 = *v27;
  if ( &v31 != v27 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, v27);
    v18 = v31;
    v19 = v32;
    v27[1] = v32;
    *v27 = v18;
    v17 = sub_14083D4F0(v19) + 8;
    v32 = 0;
    v31 = v17;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, &v31);
  return sub_14083B0A0(&v28);
}
