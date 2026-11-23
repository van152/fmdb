__int64 __fastcall sub_140F53A10(__int64 a1, int a2, __int64 a3)
{
  unsigned __int64 v3; // rbp
  _DWORD *v7; // rdi
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  volatile signed __int32 *v9; // rcx
  __int64 v10; // rcx
  __int64 *v12; // r15
  __int64 v13; // r14
  __int64 v14; // rcx
  unsigned __int64 v15; // rsi
  unsigned __int64 v16; // rdx
  unsigned __int64 v17; // r8
  unsigned __int64 v18; // rax
  unsigned __int64 v19; // rdi
  unsigned __int64 v20; // rcx
  __int64 v21; // r8
  __int64 v22; // rdi
  bool v23; // al
  __int64 v24; // rsi
  __int64 v25; // r15
  __int64 v26; // rbp
  __int64 v27; // rbx
  __int64 v28; // rdi
  unsigned __int64 v29; // rcx
  __int64 v30; // r8
  __int64 v31; // r14
  bool v32; // al
  __int64 v33; // rdi
  volatile signed __int32 *v34; // rsi
  __int64 v35; // rax
  __int64 v36; // r8
  __int64 v37; // rax
  volatile signed __int32 *v38; // rsi
  volatile signed __int32 *v39; // rsi
  int v40; // [rsp+30h] [rbp-98h]
  volatile signed __int32 *v41; // [rsp+48h] [rbp-80h] BYREF
  unsigned int v42; // [rsp+54h] [rbp-74h] BYREF
  char v43[8]; // [rsp+58h] [rbp-70h] BYREF
  int v44; // [rsp+60h] [rbp-68h] BYREF
  volatile signed __int32 *v45; // [rsp+68h] [rbp-60h] BYREF
  __int64 v46; // [rsp+70h] [rbp-58h] BYREF
  unsigned __int64 v47; // [rsp+78h] [rbp-50h]
  unsigned __int64 v48; // [rsp+80h] [rbp-48h]

  v46 = 0;
  if ( (*(_BYTE *)(a1 + 92) & 2) != 0 )
  {
    *(_BYTE *)(a1 + 89) = 1;
    LOBYTE(v3) = 1;
    return (unsigned int)v3;
  }
  sub_14080D0E0(a1: &v44, a2: 0x1418E2C24LL);
  LODWORD(v3) = 0;
  sub_140FFADB0(a1, a2: &v46, a3: 0, a4: 0);
  v41 = (volatile signed __int32 *)0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v41,
    a2: (unsigned int)&v45,
    a3: a2,
    a4: (unsigned int)&v46,
    a5: (__int64)&v44,
    a6: 0,
    a7: 0,
    0);
  if ( v45 != nullptr )
  {
    v41 = v45;
    _InterlockedIncrement(v45 + 2);
    v7 = v41;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v41 + 40LL))(
      a1: v41,
      a2: &v42,
      a3: 4);
    if ( v7[4] == 0 )
    {
      (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 92, a3: 1);
      if ( v7[4] == 0 )
      {
        if ( v42 != 0 )
        {
          v12 = *(__int64 **)(a1 + 128);
          v13 = *v12;
          v14 = v12[1];
          v3 = (v14 - *v12) >> 3;
          if ( v3 < v42 )
          {
            v15 = v42 - 1;
            if ( v3 > v15 && *(_QWORD *)(v13 + 8 * v15) != 0 )
            {
              sub_140FB2020(a1: *(_QWORD *)(v13 + 8 * v15));
              v13 = *v12;
              v14 = v12[1];
              v3 = (v14 - *v12) >> 3;
            }
            if ( v3 <= v15 )
            {
              v16 = v15 + 1;
              v17 = v15 + 1 - v3;
              if ( v15 + 1 >= v3 )
              {
                v18 = (v12[2] - v13) >> 3;
                if ( v18 <= v15 )
                {
                  v19 = v18 + (v18 >> 1);
                  v48 = v15 + 1;
                  if ( v19 <= v16 )
                    v19 = v15 + 1;
                  v47 = v19;
                  v13 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v19);
                  sub_141758A10(a1: v13 + 8 * v3, a2: 0, a3: 8 * (v15 + 1 - v3));
                  sub_141758A00(a1: v13, a2: *v12, a3: v12[1] - *v12);
                  v3 = *v12;
                  if ( *v12 != 0 )
                  {
                    v20 = v12[2] - v3;
                    if ( v20 == -1 )
                      v20 = *(unsigned int *)(v3 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v21 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v21) >> 3 > v20)
                      && (v22 = *(_QWORD *)(v21 + 8 * v20)) != 0 )
                    {
                      v3 -= *(unsigned int *)(v22 + 120);
                      MEMORY[0x1419475D8](a1: v22 + 32, a2: v3);
                      v23 = *(_BYTE *)(v22 + 72) != 0
                         && _InterlockedDecrement((volatile signed __int32 *)(v22 + 64)) != 0;
                      if ( !v23 && *(_BYTE *)(v22 + 97) != 0 )
                        sub_1412D33C0(a1: v22);
                    }
                    else
                    {
                      v3 -= *(unsigned int *)(qword_141ABD470 + 48);
                      MEMORY[0x141948990](a1: v3);
                    }
                  }
                  *v12 = v13;
                  v12[1] = v13 + 8 * v48;
                  v12[2] = v13 + 8 * v47;
                }
                else
                {
                  v3 = v14 + 8 * v17;
                  sub_141758A10(a1: v14, a2: 0, a3: 8 * v17);
                  v12[1] = v3;
                  v13 = *v12;
                }
              }
              else
              {
                v12[1] = v13 + 8 * v16;
              }
            }
            *(_QWORD *)(v13 + 8 * v15) = 0;
          }
        }
        if ( (*(_BYTE *)(a1 + 92) & 1) != 0 )
        {
          v24 = v42;
          v25 = *(_QWORD *)(a1 + 136);
          if ( (*(_QWORD *)(a1 + 152) - v25) >> 3 < (unsigned __int64)v42 )
          {
            v26 = *(_QWORD *)(a1 + 144);
            v27 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v42);
            sub_141758A00(a1: v27, a2: *(_QWORD *)(a1 + 136), a3: *(_QWORD *)(a1 + 144) - *(_QWORD *)(a1 + 136));
            v28 = *(_QWORD *)(a1 + 136);
            if ( v28 != 0 )
            {
              v29 = *(_QWORD *)(a1 + 152) - v28;
              if ( v29 == -1 )
                v29 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v30 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v30) >> 3 > v29)
                && (v31 = *(_QWORD *)(v30 + 8 * v29)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v31 + 32, a2: v28 - *(unsigned int *)(v31 + 120));
                v32 = *(_BYTE *)(v31 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) != 0;
                if ( !v32 && *(_BYTE *)(v31 + 97) != 0 )
                  sub_1412D33C0(a1: v31);
              }
              else
              {
                MEMORY[0x141948990](a1: v28 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *(_QWORD *)(a1 + 136) = v27;
            v3 = v27 + v26 - v25;
            *(_QWORD *)(a1 + 144) = v3;
            *(_QWORD *)(a1 + 152) = v27 + 8 * v24;
          }
        }
        if ( v42 != 0 )
        {
          v33 = 0;
          while ( 1 )
          {
            v34 = v41;
            (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v41 + 40LL))(
              a1: v41,
              a2: &v44,
              a3: 1);
            if ( *((_DWORD *)v34 + 4) != 0 )
              break;
            v35 = sub_140F49530(a1: *(unsigned int *)(a1 + 84), a2: (unsigned __int8)v44);
            if ( v35 != 0 )
            {
              v3 = *(_QWORD *)v35;
              LOBYTE(v40) = 1;
              LOBYTE(v36) = 1;
              if ( (*(unsigned __int8 (__fastcall **)(__int64, volatile signed __int32 **, __int64, __int64, _DWORD, _DWORD, int, __int64))(*(_QWORD *)v35 + 152LL))(
                     a1: v35,
                     a2: &v41,
                     a3: v36,
                     a4: a3,
                     a5: *(_DWORD *)(a1 + 84),
                     a6: v33,
                     a7: v40,
                     a8: a1) == 0 )
                break;
            }
            if ( ++v33 >= (unsigned __int64)v42 )
              goto LABEL_59;
          }
        }
        else
        {
LABEL_59:
          v37 = *(_QWORD *)(a1 + 8);
          if ( v37 != *(_QWORD *)(a1 + 16) )
            *(_QWORD *)(a1 + 16) = v37;
          sub_140FFAFD0(a1: &v44, a2: &v41, a3: a1 + 8, a4: v43);
          if ( v44 == 0 )
          {
            v38 = v41;
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v41 + 40LL))(
              a1: v41,
              a2: a1 + 88,
              a3: 1);
            if ( *((_DWORD *)v38 + 4) == 0 )
            {
              v39 = v41;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v41 + 40LL))(
                a1: v41,
                a2: a1 + 80,
                a3: 4);
              if ( *((_DWORD *)v39 + 4) == 0 )
              {
                *(_WORD *)(a1 + 89) = 1;
                LOBYTE(v3) = 1;
LABEL_6:
                v8 = (void (__fastcall ***)(_QWORD, __int64))v41;
                if ( v41 != nullptr && _InterlockedDecrement(v41 + 2) == 0 )
                  (**v8)(a1: v8, a2: 1);
                v9 = v45;
                if ( v45 != nullptr && _InterlockedDecrement(v45 + 2) == 0 )
                  (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v9)(a1: v9, a2: 1);
                goto LABEL_12;
              }
            }
          }
        }
      }
    }
    LODWORD(v3) = 0;
    goto LABEL_6;
  }
LABEL_12:
  v10 = v46;
  if ( v46 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v46 - 4)) == 0 )
    sub_1412EC9A0(a1: v10 - 4);
  return (unsigned int)v3;
}
