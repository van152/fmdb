__int64 __fastcall sub_141189030(__int64 a1, __int64 *a2)
{
  __int64 *v2; // rax
  __int64 v3; // r15
  __int64 result; // rax
  __int64 v5; // r15
  __int64 v8; // r15
  __int64 v9; // r14
  __int64 (__fastcall *v10)(_QWORD, _QWORD); // r10
  void *v11; // r11
  __int64 *v12; // rdx
  __int64 v13; // rcx
  __int64 v14; // rdx
  __int64 v15; // r12
  __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 *v18; // rdx
  bool v19; // zf
  __int64 v20; // rbx
  __int64 (__fastcall *v21)(_QWORD, _QWORD); // r13
  void *v22; // rbp
  __int64 v23; // rax
  _QWORD *v24; // rbx
  __int64 v25; // rbp
  unsigned __int64 v26; // rax
  unsigned __int64 v27; // r13
  __int64 v28; // rsi
  _QWORD *v29; // r12
  __int64 v30; // r12
  __int64 v31; // rbx
  unsigned __int64 v32; // rcx
  __int64 v33; // rbp
  __int64 v34; // rbp
  bool v35; // al
  __int64 v36; // rcx
  __int64 (__fastcall *v37)(_QWORD, _QWORD); // rbx
  void *v38; // rbp
  __int64 v39; // rbp
  __int64 v40; // r8
  unsigned __int64 v41; // r8
  __int64 v42; // rdx
  __int64 v43; // rdx
  unsigned __int64 v44; // rbx
  __int64 v45; // rcx
  __int64 v46; // [rsp+28h] [rbp-50h]
  unsigned __int64 v47; // [rsp+30h] [rbp-48h]

  v2 = *(__int64 **)(qword_141B5FE40 + 128);
  v3 = v2[1];
  result = *v2;
  v5 = v3 - result;
  if ( v5 != 0 )
  {
    v8 = v5 >> 3;
    v9 = 0;
    v10 = MEMORY[0x1419475D8];
    v11 = &unk_141AADAD0;
    do
    {
      if ( (int)v9 < 0 )
        goto LABEL_4;
      result = (unsigned int)v9;
      if ( (_BYTE)word_141B60320 != 0 )
      {
        v12 = *(__int64 **)(qword_141B5FE40 + 128);
        v13 = *v12;
        v14 = v12[1];
      }
      else
      {
        v13 = *(_QWORD *)(qword_141B5FE40 + 96);
        v14 = *(_QWORD *)(qword_141B5FE40 + 104);
      }
      if ( (v14 - v13) >> 3 <= (unsigned __int64)(unsigned int)v9 )
        goto LABEL_4;
      v15 = *(_QWORD *)(v13 + 8LL * (unsigned int)v9);
      if ( v15 == 0 || (*(_BYTE *)(v15 + 176) & 1) != 0 )
        goto LABEL_4;
      result = *(_QWORD *)(v13 + 8LL * (unsigned int)v9);
      while ( 1 )
      {
        v16 = *(_QWORD *)(result + 120);
        if ( v16 != 0 )
          break;
        v17 = *(_QWORD *)(result + 48);
        if ( v17 != 0 )
        {
          v18 = *(__int64 **)(v17 + 24);
          if ( *(__int64 **)(v17 + 32) != v18 )
          {
            v19 = *v18 == result;
            result = *v18;
            if ( !v19 )
              continue;
          }
        }
        goto LABEL_4;
      }
      if ( v16 != a1 )
        goto LABEL_4;
      v20 = *(_QWORD *)(v15 + 48);
      if ( v20 == 0 )
        goto LABEL_24;
      result = *(unsigned __int8 *)(v20 + 186);
      if ( (_BYTE)result == 1 )
      {
        v21 = v10;
        v22 = v11;
        v23 = sub_141758910(v20, 0, (__int64)&unk_141AADB30, (__int64)v11, 0);
        v11 = v22;
        v10 = v21;
        if ( v23 != 0 )
        {
          result = *(_QWORD *)(v23 + 368);
          if ( *(_QWORD *)(result + 240) == 0 )
            goto LABEL_4;
        }
        result = *(unsigned __int8 *)(v20 + 186);
      }
      if ( (_BYTE)result != 0 )
        goto LABEL_24;
      v36 = v20;
      v37 = v10;
      v38 = v11;
      result = sub_141758910(v36, 0, (__int64)&unk_141AADB30, (__int64)&unk_141AADB10, 0);
      v11 = v38;
      v10 = v37;
      if ( result == 0 )
        goto LABEL_24;
      v39 = *(_QWORD *)(result + 24);
      v40 = *(_QWORD *)(result + 32) - v39;
      if ( v40 != 0 )
      {
        v41 = v40 >> 3;
        v42 = 1;
        if ( v41 >= 2 )
          v42 = v41;
        if ( (*(_BYTE *)(*(_QWORD *)v39 + 176LL) & 1) != 0 )
        {
          v43 = v42 - 1;
          v44 = 0;
          while ( v43 != v44 )
          {
            v45 = *(_QWORD *)(v39 + 8 * v44++ + 8);
            if ( (*(_BYTE *)(v45 + 176) & 1) == 0 )
            {
              if ( v44 >= v41 )
                goto LABEL_4;
              goto LABEL_45;
            }
          }
          goto LABEL_4;
        }
LABEL_45:
        if ( *(_QWORD *)(result + 216) != 0 )
        {
LABEL_24:
          v24 = (_QWORD *)a2[1];
          if ( v24 == (_QWORD *)a2[2] )
          {
            v46 = a1;
            v25 = (__int64)v24 - *a2;
            v26 = v25 >> 3;
            v27 = v26 + (v26 >> 1);
            v47 = (v25 >> 3) + 1;
            if ( v27 <= v47 )
              v27 = v26 + 1;
            if ( v26 > 0x1FFFFFFFFFFFFFFFLL - (v26 >> 1) )
              v27 = 0x1FFFFFFFFFFFFFFFLL;
            v28 = sub_1407E4490(qword_141ABD470, 8 * v27);
            *(_QWORD *)(v28 + v25) = v15;
            v29 = (_QWORD *)a2[1];
            sub_141758A00();
            if ( v29 != v24 )
              sub_141758A00();
            v30 = v28;
            v31 = *a2;
            a1 = v46;
            v11 = &unk_141AADAD0;
            if ( *a2 != 0 )
            {
              v32 = a2[2] - v31;
              if ( v32 == -1 )
                v32 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0
                || (v33 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 <= v32)
                || (v34 = *(_QWORD *)(v33 + 8 * v32)) == 0 )
              {
                MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
                goto LABEL_48;
              }
              MEMORY[0x1419475D8](v34 + 32, v31 - *(unsigned int *)(v34 + 120));
              v35 = *(_BYTE *)(v34 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) != 0;
              a1 = v46;
              v11 = &unk_141AADAD0;
              if ( !v35 && *(_BYTE *)(v34 + 97) != 0 )
              {
                sub_1412D33C0(v34);
LABEL_48:
                v11 = &unk_141AADAD0;
                a1 = v46;
              }
            }
            *a2 = v30;
            a2[1] = v30 + 8 * v47;
            result = v30 + 8 * v27;
            a2[2] = result;
            v10 = MEMORY[0x1419475D8];
            goto LABEL_4;
          }
          *v24 = v15;
          a2[1] += 8;
        }
      }
LABEL_4:
      ++v9;
    }
    while ( v9 != v8 );
  }
  return result;
}
