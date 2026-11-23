int *__fastcall sub_14096BA90(int *a1, _QWORD *a2, __int64 *a3)
{
  _QWORD *v4; // r12
  __int64 v6; // rbx
  int v7; // eax
  __int64 v8; // r15
  __int64 v9; // rdi
  __int64 v10; // rsi
  __int64 v11; // rbp
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // r14
  bool v15; // al
  __int64 v16; // rsi
  int v17; // ebx
  __int64 v18; // r15
  __int64 v19; // rcx
  unsigned __int64 v20; // rdi
  unsigned __int64 v21; // rax
  int *v22; // r12
  unsigned __int64 v23; // rbp
  __int64 v24; // rdi
  unsigned __int64 v25; // rcx
  __int64 v26; // r8
  __int64 v27; // r14
  bool v28; // al
  __int64 v29; // r14
  _DWORD *v30; // rdi
  __int64 v31; // rbx
  unsigned __int64 v32; // rax
  unsigned __int64 v33; // r15
  unsigned __int64 v34; // rcx
  unsigned __int64 v35; // r15
  __int64 v36; // rsi
  _DWORD *v37; // r12
  __int64 v38; // rdi
  unsigned __int64 v39; // rcx
  __int64 v40; // rbx
  __int64 v41; // rbx
  unsigned __int64 v42; // rsi
  __int64 v43; // rdi
  __int64 v44; // rsi
  int v46; // [rsp+24h] [rbp-64h] BYREF
  unsigned int v47; // [rsp+28h] [rbp-60h] BYREF
  unsigned int v48; // [rsp+2Ch] [rbp-5Ch] BYREF
  _QWORD *v49; // [rsp+30h] [rbp-58h]
  int *v50; // [rsp+38h] [rbp-50h]
  unsigned __int64 v51; // [rsp+40h] [rbp-48h]

  v4 = a2;
  if ( a3[1] == *a3 )
  {
    v48 = 0;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v48, a3: 4);
    v16 = v48;
    v17 = 1;
    if ( qword_141AA7808 > (unsigned __int64)v48 )
    {
      v18 = *a3;
      v19 = a3[1];
      v20 = (v19 - *a3) >> 2;
      if ( v20 <= v48 )
      {
        if ( v20 < v48 )
        {
          v21 = (a3[2] - v18) >> 2;
          if ( v21 >= v48 )
          {
            v42 = v48 - v20;
            v43 = v19 + 4 * v42;
            sub_141758A10(a1: v19, a2: 0, a3: 4 * v42);
            a3[1] = v43;
            v18 = *a3;
            v19 = v43;
          }
          else
          {
            v49 = v4;
            v22 = a1;
            v23 = v21 + (v21 >> 1);
            if ( v23 <= v48 )
              v23 = v48;
            v18 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v23);
            sub_141758A10(a1: v18 + 4 * v20, a2: 0, a3: 4 * (v16 - v20));
            sub_141758A00(a1: v18, a2: *a3, a3: a3[1] - *a3);
            v24 = *a3;
            if ( *a3 != 0 )
            {
              v25 = a3[2] - v24;
              if ( v25 == -1 )
                v25 = *(unsigned int *)(v24 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v26 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v26) >> 3 > v25)
                && (v27 = *(_QWORD *)(v26 + 8 * v25)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v27 + 32, a2: v24 - *(unsigned int *)(v27 + 120));
                v28 = *(_BYTE *)(v27 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) != 0;
                if ( !v28 && *(_BYTE *)(v27 + 97) != 0 )
                  sub_1412D33C0(a1: v27);
              }
              else
              {
                MEMORY[0x141948990](a1: v24 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *a3 = v18;
            v19 = v18 + 4 * v16;
            a3[1] = v19;
            a3[2] = v18 + 4 * v23;
            a1 = v22;
            v4 = v49;
          }
        }
      }
      else
      {
        v19 = v18 + 4LL * v48;
        a3[1] = v19;
      }
      if ( (v19 - v18) >> 2 >= (unsigned __int64)v48 )
      {
        v44 = *v4;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: v18, a3: 4LL * v48);
        v17 = *(_DWORD *)(v44 + 16);
      }
    }
    *a1 = v17;
  }
  else
  {
    v47 = 0;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v47, a3: 4);
    v6 = v47;
    v7 = 1;
    if ( qword_141AA7808 > (unsigned __int64)v47 )
    {
      v50 = a1;
      v8 = *a3;
      if ( (a3[2] - *a3) >> 2 < (unsigned __int64)v47 )
      {
        v9 = a3[1];
        v10 = sub_1407E4490(a1: qword_141ABD470, a2: 4LL * v47);
        sub_141758A00(a1: v10, a2: *a3, a3: a3[1] - *a3);
        v11 = *a3;
        if ( *a3 != 0 )
        {
          v12 = a3[2] - v11;
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
        *a3 = v10;
        a3[1] = v10 + v9 - v8;
        a3[2] = v10 + 4 * v6;
        LODWORD(v6) = v47;
      }
      if ( (_DWORD)v6 != 0 )
      {
        v29 = 0;
        v49 = v4;
        while ( 1 )
        {
          v46 = 0;
          (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*v4 + 40LL))(a1: *v4, a2: &v46, a3: 4);
          if ( *(_DWORD *)(*v4 + 16LL) != 0 )
            goto LABEL_55;
          v30 = (_DWORD *)a3[1];
          if ( v30 == (_DWORD *)a3[2] )
            break;
          *v30 = v46;
          a3[1] += 4;
LABEL_32:
          if ( ++v29 >= (unsigned __int64)v47 )
            goto LABEL_55;
        }
        v31 = (__int64)v30 - *a3;
        v32 = v31 >> 2;
        v33 = (unsigned __int64)(v31 >> 2) >> 1;
        v34 = 0x3FFFFFFFFFFFFFFFLL - v33;
        v35 = (v31 >> 2) + v33;
        v51 = (v31 >> 2) + 1;
        if ( v35 <= v51 )
          v35 = v32 + 1;
        if ( v32 > v34 )
          v35 = 0x3FFFFFFFFFFFFFFFLL;
        v36 = sub_1407E4490(a1: qword_141ABD470, a2: 4 * v35);
        *(_DWORD *)(v36 + v31) = v46;
        v37 = (_DWORD *)a3[1];
        sub_141758A00(a1: v36, a2: *a3, a3: (char *)v30 - *a3);
        if ( v37 != v30 )
          sub_141758A00(a1: v36 + v31 + 4, a2: v30, a3: a3[1] - (_QWORD)v30);
        v38 = *a3;
        v4 = v49;
        if ( *a3 == 0 )
        {
LABEL_52:
          *a3 = v36;
          a3[1] = v36 + 4 * v51;
          a3[2] = v36 + 4 * v35;
          goto LABEL_32;
        }
        v39 = a3[2] - v38;
        if ( v39 == -1 )
        {
          v39 = *(unsigned int *)(v38 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          {
LABEL_51:
            MEMORY[0x141948990](a1: v38 - *(unsigned int *)(qword_141ABD470 + 48));
            goto LABEL_52;
          }
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_51;
        }
        v40 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v40) >> 3 > v39 )
        {
          v41 = *(_QWORD *)(v40 + 8 * v39);
          if ( v41 != 0 )
          {
            MEMORY[0x1419475D8](a1: v41 + 32, a2: v38 - *(unsigned int *)(v41 + 120));
            if ( (*(_BYTE *)(v41 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v41 + 64)) == 0)
              && *(_BYTE *)(v41 + 97) != 0 )
            {
              sub_1412D33C0(a1: v41);
            }
            goto LABEL_52;
          }
        }
        goto LABEL_51;
      }
LABEL_55:
      v7 = *(_DWORD *)(*v4 + 16LL);
      a1 = v50;
    }
    *a1 = v7;
  }
  return a1;
}
