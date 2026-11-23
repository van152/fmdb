__int64 __fastcall sub_140F524C0(__int64 a1, int a2, __int64 a3)
{
  unsigned __int64 v3; // rbp
  _DWORD *v7; // rdi
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  volatile signed __int32 *v9; // rcx
  __int64 v10; // rcx
  __int64 *v12; // rdi
  __int64 v13; // r14
  __int64 v14; // rcx
  unsigned __int64 v15; // rsi
  _QWORD *v16; // r15
  __int64 v17; // rcx
  __int64 v18; // rcx
  __int64 v19; // rcx
  unsigned __int64 v20; // rdx
  unsigned __int64 v21; // r15
  unsigned __int64 v22; // rax
  __int64 *v23; // r8
  unsigned __int64 v24; // rdi
  __int64 v25; // rdx
  __int64 *v26; // rdi
  unsigned __int64 v27; // rcx
  __int64 v28; // r8
  __int64 v29; // r15
  bool v30; // al
  __int64 v31; // rsi
  __int64 v32; // r15
  __int64 v33; // rbp
  __int64 v34; // rbx
  __int64 v35; // rdi
  unsigned __int64 v36; // rcx
  __int64 v37; // r8
  __int64 v38; // r14
  bool v39; // al
  __int64 v40; // rdi
  volatile signed __int32 *v41; // rsi
  __int64 v42; // rax
  __int64 v43; // r8
  __int64 v44; // rax
  volatile signed __int32 *v45; // rsi
  volatile signed __int32 *v46; // rsi
  int v47; // [rsp+30h] [rbp-98h]
  volatile signed __int32 *v48; // [rsp+48h] [rbp-80h] BYREF
  unsigned int v49; // [rsp+54h] [rbp-74h] BYREF
  char v50[8]; // [rsp+58h] [rbp-70h] BYREF
  int v51; // [rsp+60h] [rbp-68h] BYREF
  volatile signed __int32 *v52; // [rsp+68h] [rbp-60h] BYREF
  __int64 v53; // [rsp+70h] [rbp-58h] BYREF
  unsigned __int64 v54; // [rsp+78h] [rbp-50h]
  unsigned __int64 v55; // [rsp+80h] [rbp-48h]

  v53 = 0;
  if ( (*(_BYTE *)(a1 + 92) & 2) != 0 )
  {
    *(_BYTE *)(a1 + 89) = 1;
    LOBYTE(v3) = 1;
    return (unsigned int)v3;
  }
  sub_14080D0E0(a1: &v51, a2: 0x1418E2C24LL);
  LODWORD(v3) = 0;
  sub_140FFADB0(a1, a2: &v53, a3: 0, a4: 0);
  v48 = (volatile signed __int32 *)0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v48,
    a2: (unsigned int)&v52,
    a3: a2,
    a4: (unsigned int)&v53,
    a5: (__int64)&v51,
    a6: 0,
    a7: 0,
    0);
  if ( v52 != nullptr )
  {
    v48 = v52;
    _InterlockedIncrement(v52 + 2);
    v7 = v48;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v48 + 40LL))(
      a1: v48,
      a2: &v49,
      a3: 4);
    if ( v7[4] == 0 )
    {
      (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 92, a3: 1);
      if ( v7[4] == 0 )
      {
        if ( v49 != 0 )
        {
          v12 = *(__int64 **)(a1 + 128);
          v13 = *v12;
          v14 = v12[1];
          v3 = (v14 - *v12) >> 3;
          if ( v3 < v49 )
          {
            v15 = v49 - 1;
            if ( v3 > v15 )
            {
              v16 = *(_QWORD **)(v13 + 8 * v15);
              if ( v16 != nullptr )
              {
                v17 = v16[12];
                if ( v17 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17 - 4)) == 0 )
                  sub_1412EC9A0(a1: v17 - 4);
                v18 = v16[11];
                if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 - 4)) == 0 )
                  sub_1412EC9A0(a1: v18 - 4);
                v19 = v16[10];
                if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 - 4)) == 0 )
                  sub_1412EC9A0(a1: v19 - 4);
                sub_140FAF440(a1: v16);
                v13 = *v12;
                v14 = v12[1];
                v3 = (v14 - *v12) >> 3;
              }
            }
            if ( v3 <= v15 )
            {
              v20 = v15 + 1;
              v21 = v15 + 1 - v3;
              if ( v15 + 1 >= v3 )
              {
                v22 = (v12[2] - v13) >> 3;
                if ( v22 <= v15 )
                {
                  v23 = v12;
                  v24 = v22 + (v22 >> 1);
                  v55 = v15 + 1;
                  if ( v24 <= v20 )
                    v24 = v15 + 1;
                  v54 = v24;
                  v25 = 8 * v24;
                  v26 = v23;
                  v13 = sub_1407E4490(a1: qword_141ABD470, a2: v25);
                  sub_141758A10(a1: v13 + 8 * v3, a2: 0, a3: 8 * v21);
                  sub_141758A00(a1: v13, a2: *v26, a3: v26[1] - *v26);
                  v3 = *v26;
                  if ( *v26 != 0 )
                  {
                    v27 = v26[2] - v3;
                    if ( v27 == -1 )
                      v27 = *(unsigned int *)(v3 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v28 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v28) >> 3 > v27)
                      && (v29 = *(_QWORD *)(v28 + 8 * v27)) != 0 )
                    {
                      v3 -= *(unsigned int *)(v29 + 120);
                      MEMORY[0x1419475D8](a1: v29 + 32, a2: v3);
                      v30 = *(_BYTE *)(v29 + 72) != 0
                         && _InterlockedDecrement((volatile signed __int32 *)(v29 + 64)) != 0;
                      if ( !v30 && *(_BYTE *)(v29 + 97) != 0 )
                        sub_1412D33C0(a1: v29);
                    }
                    else
                    {
                      v3 -= *(unsigned int *)(qword_141ABD470 + 48);
                      MEMORY[0x141948990](a1: v3);
                    }
                  }
                  *v26 = v13;
                  v26[1] = v13 + 8 * v55;
                  v26[2] = v13 + 8 * v54;
                }
                else
                {
                  v3 = v14 + 8 * v21;
                  sub_141758A10(a1: v14, a2: 0, a3: 8 * v21);
                  v12[1] = v3;
                  v13 = *v12;
                }
              }
              else
              {
                v12[1] = v13 + 8 * v20;
              }
            }
            *(_QWORD *)(v13 + 8 * v15) = 0;
          }
        }
        if ( (*(_BYTE *)(a1 + 92) & 1) != 0 )
        {
          v31 = v49;
          v32 = *(_QWORD *)(a1 + 136);
          if ( (*(_QWORD *)(a1 + 152) - v32) >> 3 < (unsigned __int64)v49 )
          {
            v33 = *(_QWORD *)(a1 + 144);
            v34 = sub_1407E4490(a1: qword_141ABD470, a2: 8LL * v49);
            sub_141758A00(a1: v34, a2: *(_QWORD *)(a1 + 136), a3: *(_QWORD *)(a1 + 144) - *(_QWORD *)(a1 + 136));
            v35 = *(_QWORD *)(a1 + 136);
            if ( v35 != 0 )
            {
              v36 = *(_QWORD *)(a1 + 152) - v35;
              if ( v36 == -1 )
                v36 = *(unsigned int *)(v35 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v37 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v37) >> 3 > v36)
                && (v38 = *(_QWORD *)(v37 + 8 * v36)) != 0 )
              {
                MEMORY[0x1419475D8](a1: v38 + 32, a2: v35 - *(unsigned int *)(v38 + 120));
                v39 = *(_BYTE *)(v38 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38 + 64)) != 0;
                if ( !v39 && *(_BYTE *)(v38 + 97) != 0 )
                  sub_1412D33C0(a1: v38);
              }
              else
              {
                MEMORY[0x141948990](a1: v35 - *(unsigned int *)(qword_141ABD470 + 48));
              }
            }
            *(_QWORD *)(a1 + 136) = v34;
            v3 = v34 + v33 - v32;
            *(_QWORD *)(a1 + 144) = v3;
            *(_QWORD *)(a1 + 152) = v34 + 8 * v31;
          }
        }
        if ( v49 != 0 )
        {
          v40 = 0;
          while ( 1 )
          {
            v41 = v48;
            (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v48 + 40LL))(
              a1: v48,
              a2: &v51,
              a3: 1);
            if ( *((_DWORD *)v41 + 4) != 0 )
              break;
            v42 = sub_140F49530(a1: *(unsigned int *)(a1 + 84), a2: (unsigned __int8)v51);
            if ( v42 != 0 )
            {
              v3 = *(_QWORD *)v42;
              LOBYTE(v47) = 1;
              LOBYTE(v43) = 1;
              if ( (*(unsigned __int8 (__fastcall **)(__int64, volatile signed __int32 **, __int64, __int64, _DWORD, _DWORD, int, __int64))(*(_QWORD *)v42 + 152LL))(
                     a1: v42,
                     a2: &v48,
                     a3: v43,
                     a4: a3,
                     a5: *(_DWORD *)(a1 + 84),
                     a6: v40,
                     a7: v47,
                     a8: a1) == 0 )
                break;
            }
            if ( ++v40 >= (unsigned __int64)v49 )
              goto LABEL_68;
          }
        }
        else
        {
LABEL_68:
          v44 = *(_QWORD *)(a1 + 8);
          if ( v44 != *(_QWORD *)(a1 + 16) )
            *(_QWORD *)(a1 + 16) = v44;
          sub_140FFAFD0(a1: &v51, a2: &v48, a3: a1 + 8, a4: v50);
          if ( v51 == 0 )
          {
            v45 = v48;
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v48 + 40LL))(
              a1: v48,
              a2: a1 + 88,
              a3: 1);
            if ( *((_DWORD *)v45 + 4) == 0 )
            {
              v46 = v48;
              (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v48 + 40LL))(
                a1: v48,
                a2: a1 + 80,
                a3: 4);
              if ( *((_DWORD *)v46 + 4) == 0 )
              {
                *(_WORD *)(a1 + 89) = 1;
                LOBYTE(v3) = 1;
LABEL_6:
                v8 = (void (__fastcall ***)(_QWORD, __int64))v48;
                if ( v48 != nullptr && _InterlockedDecrement(v48 + 2) == 0 )
                  (**v8)(a1: v8, a2: 1);
                v9 = v52;
                if ( v52 != nullptr && _InterlockedDecrement(v52 + 2) == 0 )
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
  v10 = v53;
  if ( v53 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v53 - 4)) == 0 )
    sub_1412EC9A0(a1: v10 - 4);
  return (unsigned int)v3;
}
