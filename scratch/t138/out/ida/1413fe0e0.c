char __fastcall sub_1413FE0E0(__int64 *a1, _QWORD *a2)
{
  _QWORD *v2; // r14
  __int64 v4; // rsi
  char result; // al
  unsigned __int8 v6; // dl
  __int64 v7; // rbx
  __int64 v8; // r15
  unsigned __int64 v9; // rcx
  __int64 v10; // rdi
  __int64 v11; // r12
  __int64 v12; // rsi
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // r14
  bool v16; // al
  __int64 v17; // r15
  __int64 v18; // rbx
  __int64 v19; // rax
  __int64 *v20; // rdi
  __int64 v21; // r14
  unsigned __int64 v22; // rax
  unsigned __int64 v23; // r12
  unsigned __int64 v24; // rcx
  unsigned __int64 v25; // r12
  __int64 v26; // rsi
  __int64 *v27; // rbx
  __int64 v28; // rdi
  unsigned __int64 v29; // rcx
  __int64 v30; // rbx
  __int64 v31; // rbx
  unsigned __int64 v32; // [rsp+20h] [rbp-40h]
  _QWORD v33[2]; // [rsp+28h] [rbp-38h] BYREF
  _QWORD *v34; // [rsp+38h] [rbp-28h]
  unsigned __int8 v35; // [rsp+47h] [rbp-19h] BYREF
  __int64 v36; // [rsp+48h] [rbp-18h]

  v36 = -2;
  v2 = a2;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v35, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  v6 = v35;
  v7 = v35;
  v8 = *a1;
  v9 = (a1[2] - *a1) >> 3;
  v34 = v2;
  if ( v9 < v35 )
  {
    v10 = a1[1];
    v11 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v35);
    sub_141758A00(a1: v11, a2: *a1, a3: a1[1] - *a1);
    v12 = *a1;
    if ( *a1 != 0 )
    {
      v13 = a1[2] - v12;
      if ( v13 == -1 )
        v13 = *(unsigned int *)(v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v14 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13)
        && (v15 = *(_QWORD *)(v14 + 8 * v13)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v15 + 32, a2: v12 - *(unsigned int *)(v15 + 120));
        v16 = *(_BYTE *)(v15 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 64)) != 0;
        if ( !v16 && *(_BYTE *)(v15 + 97) != 0 )
          sub_1412D33C0(a1: v15);
      }
      else
      {
        MEMORY[0x141948990](a1: v12 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *a1 = v11;
    a1[1] = v11 + v10 - v8;
    a1[2] = v11 + 8 * v7;
    v6 = v35;
    v2 = v34;
  }
  result = 1;
  if ( v6 != 0 )
  {
    v17 = 0;
    while ( 1 )
    {
      v18 = sub_141750CC0(a1: 48);
      *(_OWORD *)v18 = 0;
      *(_OWORD *)(v18 + 16) = 0;
      *(_OWORD *)(v18 + 32) = 0;
      *(_QWORD *)v18 = 0x1418B5BB8LL;
      v19 = sub_14083D4F0();
      v33[1] = 0;
      v33[0] = v19 + 8;
      (*(void (__fastcall **)(__int64, _QWORD *, __int64))(*(_QWORD *)(v19 + 8) + 24LL))(
        a1: v19 + 8,
        a2: v33,
        a3: v18 + 16);
      *(_DWORD *)(v18 + 8) = -8388609;
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v33[0] + 16LL))(a1: v33[0], a2: v33);
      *(_QWORD *)(v18 + 32) = 0x76C0001076C0001LL;
      *(_DWORD *)(v18 + 40) = -1;
      *(_WORD *)(v18 + 44) = 0;
      if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v18 + 24LL))(a1: v18, a2: v2) == 0 )
      {
        (**(void (__fastcall ***)(__int64, __int64))v18)(a1: v18, a2: 1);
        return 0;
      }
      v20 = (__int64 *)a1[1];
      if ( v20 == (__int64 *)a1[2] )
        break;
      *v20 = v18;
      a1[1] += 8;
LABEL_18:
      if ( ++v17 >= (unsigned __int64)v35 )
        return 1;
    }
    v21 = (__int64)v20 - *a1;
    v22 = v21 >> 3;
    v23 = (unsigned __int64)(v21 >> 3) >> 1;
    v24 = 0x1FFFFFFFFFFFFFFFLL - v23;
    v25 = (v21 >> 3) + v23;
    v32 = (v21 >> 3) + 1;
    if ( v25 <= v32 )
      v25 = v22 + 1;
    if ( v22 > v24 )
      v25 = 0x1FFFFFFFFFFFFFFFLL;
    v26 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v25);
    *(_QWORD *)(v26 + v21) = v18;
    v27 = (__int64 *)a1[1];
    sub_141758A00(a1: v26, a2: *a1, a3: (char *)v20 - *a1);
    if ( v27 != v20 )
      sub_141758A00(a1: v26 + v21 + 8, a2: v20, a3: a1[1] - (_QWORD)v20);
    v28 = *a1;
    v2 = v34;
    if ( *a1 == 0 )
    {
LABEL_38:
      *a1 = v26;
      a1[1] = v26 + 8 * v32;
      a1[2] = v26 + 8 * v25;
      goto LABEL_18;
    }
    v29 = a1[2] - v28;
    if ( v29 == -1 )
    {
      v29 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_37:
        MEMORY[0x141948990](a1: v28 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_38;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_37;
    }
    v30 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29 )
    {
      v31 = *(_QWORD *)(v30 + 8 * v29);
      if ( v31 != 0 )
      {
        MEMORY[0x1419475D8](a1: v31 + 32, a2: v28 - *(unsigned int *)(v31 + 120));
        if ( (*(_BYTE *)(v31 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) == 0)
          && *(_BYTE *)(v31 + 97) != 0 )
        {
          sub_1412D33C0(a1: v31);
        }
        goto LABEL_38;
      }
    }
    goto LABEL_37;
  }
  return result;
}
