char __fastcall sub_1413FECE0(__int64 *a1, _QWORD *a2)
{
  _QWORD *v2; // rdi
  __int64 v4; // rsi
  char result; // al
  unsigned __int8 v6; // dl
  __int64 v7; // rbp
  __int64 v8; // r15
  __int64 v9; // rsi
  __int64 v10; // r12
  __int64 v11; // rbx
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // r15
  __int64 v17; // rsi
  __int64 v18; // rsi
  unsigned __int8 v19; // bl
  __int16 v20; // r12
  _WORD *v21; // rbp
  __int64 v22; // rsi
  unsigned __int64 v23; // rcx
  unsigned __int64 v24; // r14
  __int16 v25; // di
  __int16 v26; // bx
  __int64 v27; // r12
  _WORD *v28; // rbx
  __int64 v29; // rbx
  _QWORD *v30; // rsi
  unsigned __int64 v31; // rcx
  __int64 v32; // rbp
  __int64 v33; // rdi
  bool v34; // al
  unsigned __int8 v35; // [rsp+25h] [rbp-53h] BYREF
  unsigned __int8 v36; // [rsp+26h] [rbp-52h] BYREF
  unsigned __int8 v37; // [rsp+27h] [rbp-51h] BYREF
  _QWORD *v38; // [rsp+28h] [rbp-50h]
  unsigned __int64 v39; // [rsp+30h] [rbp-48h]

  v2 = a2;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v35, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  v6 = v35;
  v7 = v35;
  v8 = *a1;
  if ( (a1[2] - *a1) >> 1 < (unsigned __int64)v35 )
  {
    v9 = a1[1];
    v10 = sub_1407E4490(a1: qword_141ABD470, a2: 2LL * v35);
    sub_141758A00(a1: v10, a2: *a1, a3: a1[1] - *a1);
    v11 = *a1;
    if ( *a1 != 0 )
    {
      v12 = a1[2] - v11;
      if ( v12 == -1 )
        v12 = *(unsigned int *)(v11 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v13 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12)
        && (v14 = *(_QWORD *)(v13 + 8 * v12)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v14 + 32, a2: v11 - *(unsigned int *)(v14 + 120));
        v15 = *(_BYTE *)(v14 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 64)) != 0;
        if ( !v15 && *(_BYTE *)(v14 + 97) != 0 )
          sub_1412D33C0(a1: v14);
      }
      else
      {
        MEMORY[0x141948990](a1: v11 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *a1 = v10;
    a1[1] = v10 + v9 - v8;
    a1[2] = v10 + 2 * v7;
    v6 = v35;
  }
  result = 1;
  if ( v6 != 0 )
  {
    v16 = 0;
    v38 = v2;
    while ( 1 )
    {
      v17 = *v2;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v37, a3: 1);
      if ( *(_DWORD *)(v17 + 16) != 0 )
        return 0;
      v18 = *v2;
      (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*v2 + 40LL))(a1: *v2, a2: &v36, a3: 1);
      if ( *(_DWORD *)(v18 + 16) != 0 )
        return 0;
      v19 = v37;
      v20 = v36;
      if ( (unsigned __int8)sub_1413FEB40(a1: v37) != 0 )
      {
        v21 = (_WORD *)a1[1];
        if ( v21 == (_WORD *)a1[2] )
        {
          v22 = (__int64)v21 - *a1;
          v23 = v22 >> 1;
          v24 = (v22 >> 1) + ((unsigned __int64)(v22 >> 1) >> 1);
          v39 = (v22 >> 1) + 1;
          if ( v24 <= v39 )
            v24 = v23 + 1;
          if ( v23 > (((unsigned __int64)(v22 >> 1) >> 1) ^ 0x7FFFFFFFFFFFFFFFLL) )
            v24 = 0x7FFFFFFFFFFFFFFFLL;
          v25 = v19;
          v26 = v20;
          v27 = sub_1407E4490(a1: qword_141ABD470, a2: 2 * v24);
          *(_WORD *)(v27 + v22) = v25 | (v26 << 8);
          v28 = (_WORD *)a1[1];
          sub_141758A00(a1: v27, a2: *a1, a3: (char *)v21 - *a1);
          if ( v28 != v21 )
            sub_141758A00(a1: v27 + v22 + 2, a2: v21, a3: a1[1] - (_QWORD)v21);
          v29 = *a1;
          v30 = v38;
          if ( *a1 != 0 )
          {
            v31 = a1[2] - v29;
            if ( v31 == -1 )
            {
              v31 = *(unsigned int *)(v29 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_38;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_38;
            }
            v32 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v32) >> 3 > v31 && (v33 = *(_QWORD *)(v32 + 8 * v31)) != 0 )
            {
              MEMORY[0x1419475D8](a1: v33 + 32, a2: v29 - *(unsigned int *)(v33 + 120));
              v34 = *(_BYTE *)(v33 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v33 + 64)) != 0;
              if ( !v34 && *(_BYTE *)(v33 + 97) != 0 )
                sub_1412D33C0(a1: v33);
            }
            else
            {
LABEL_38:
              MEMORY[0x141948990](a1: v29 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          *a1 = v27;
          a1[1] = v27 + 2 * v39;
          a1[2] = v27 + 2 * v24;
          v2 = v30;
          goto LABEL_18;
        }
        *v21 = (v20 << 8) | v19;
        a1[1] += 2;
      }
LABEL_18:
      if ( ++v16 >= (unsigned __int64)v35 )
        return 1;
    }
  }
  return result;
}
