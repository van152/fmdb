__int64 __fastcall sub_140B10980(__int64 a1, _QWORD *a2)
{
  unsigned __int64 v2; // rsi
  int v5; // r9d
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rdi
  _DWORD *v8; // rdi
  __int64 v10; // rax
  __int64 v11; // rbx
  __int64 v12; // rdi
  __int64 v13; // rdi
  __int64 v14; // rdi
  __int64 v15; // rdi
  __int64 v16; // rdi
  __int64 v17; // rdi
  __int64 v18; // rdi
  __int64 v19; // rdi
  __int64 v20; // rax
  _QWORD *v21; // rdi
  __int64 v22; // rbx
  __int64 v23; // rbx
  __int64 v24; // rbx
  __int64 v25; // rbx
  __int64 *v26; // r14
  _QWORD *v27; // rbx
  __int64 v28; // rdi
  __int64 v29; // rdi
  __int64 v30; // rdi
  __int64 v31; // rdi
  __int64 *v32; // rcx
  __int64 *v33; // rax
  _QWORD *v34; // rcx
  __int64 v35; // [rsp+28h] [rbp-28h] BYREF
  char v36[8]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v37; // [rsp+38h] [rbp-18h] BYREF
  _QWORD v38[8]; // [rsp+40h] [rbp-10h] BYREF

  v38[1] = -2;
  sub_14080D0E0(a1: v36, a2: 0x1418E2C24LL);
  v35 = 0x80100004E554C4CLL;
  if ( *a2 != 0 )
  {
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
      a1: *a2,
      a2: &v37,
      a3: &qword_141B5B720,
      a4: v36);
    if ( v37 != 0 )
    {
      LOWORD(v5) = 4;
      sub_1407D1280(a1: (unsigned int)&v35, a2: (unsigned int)v38, a3: (unsigned int)&v37, a4: v5, a5: 0);
      v6 = (void (__fastcall ***)(_QWORD, __int64))v37;
      if ( v37 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v37 + 8)) == 0 )
        (**v6)(a1: v6, a2: 1);
      v7 = v38[0];
      if ( v38[0] != 0 )
      {
        LODWORD(v37) = (*(_QWORD *)(a1 + 40) - *(_QWORD *)(a1 + 32)) >> 3;
        (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v38[0] + 40LL))(a1: v38[0], a2: &v37, a3: 4);
        if ( *(_DWORD *)(v7 + 16) == 0 )
        {
          v10 = *(_QWORD *)(a1 + 32);
          if ( *(_QWORD *)(a1 + 40) == v10 )
          {
LABEL_24:
            v19 = v38[0];
            LODWORD(v37) = (*(_QWORD *)(a1 + 64) - *(_QWORD *)(a1 + 56)) >> 3;
            (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v38[0] + 40LL))(a1: v38[0], a2: &v37, a3: 4);
            if ( *(_DWORD *)(v19 + 16) == 0 )
            {
              v20 = *(_QWORD *)(a1 + 56);
              if ( *(_QWORD *)(a1 + 64) == v20 )
              {
                v8 = (_DWORD *)v38[0];
LABEL_38:
                LODWORD(v37) = *(_DWORD *)(a1 + 88);
                (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: &v37, a3: 4);
                if ( v8[4] == 0 )
                {
                  v26 = *(__int64 **)(a1 + 80);
                  v27 = (_QWORD *)*v26;
                  LOBYTE(v2) = 1;
                  if ( (__int64 *)*v26 == v26 )
                    goto LABEL_9;
                  while ( 1 )
                  {
                    v28 = v38[0];
                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                      a1: v38[0],
                      a2: (__int64)v27 + 30,
                      a3: 2);
                    if ( *(_DWORD *)(v28 + 16) != 0 )
                      break;
                    v29 = v38[0];
                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                      a1: v38[0],
                      a2: (__int64)v27 + 28,
                      a3: 1);
                    if ( *(_DWORD *)(v29 + 16) != 0 )
                      break;
                    v30 = v38[0];
                    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                      a1: v38[0],
                      a2: (__int64)v27 + 26,
                      a3: 2);
                    if ( *(_DWORD *)(v30 + 16) != 0 )
                      break;
                    v31 = v38[0];
                    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v38[0] + 40LL))(
                      a1: v38[0],
                      a2: v27 + 4,
                      a3: 2);
                    if ( *(_DWORD *)(v31 + 16) != 0 )
                      break;
                    v32 = (__int64 *)v27[2];
                    if ( *((_BYTE *)v32 + 25) != 0 )
                    {
                      do
                      {
                        v33 = (__int64 *)v27[1];
                        if ( *((_BYTE *)v33 + 25) != 0 )
                          break;
                        v34 = v27;
                        v27 = (_QWORD *)v27[1];
                      }
                      while ( v34 == (_QWORD *)v33[2] );
                    }
                    else
                    {
                      do
                      {
                        v33 = v32;
                        v32 = (__int64 *)*v32;
                      }
                      while ( *((_BYTE *)v32 + 25) == 0 );
                    }
                    v27 = v33;
                    if ( v33 == v26 )
                      goto LABEL_9;
                  }
                }
              }
              else
              {
                v2 = 0;
                while ( 1 )
                {
                  v21 = *(_QWORD **)(v20 + 8 * v2);
                  if ( *v21 == 0 )
                    break;
                  LOBYTE(v37) = 0;
                  v22 = v38[0];
                  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v38[0] + 40LL))(
                    a1: v38[0],
                    a2: &v37,
                    a3: 1);
                  if ( *(_DWORD *)(v22 + 16) != 0 )
                    break;
                  v23 = v38[0];
                  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)v38[0] + 40LL))(
                    a1: v38[0],
                    a2: v21 + 2,
                    a3: 4);
                  if ( *(_DWORD *)(v23 + 16) != 0 )
                    break;
                  if ( (unsigned __int8)sub_1413C66C0(a1: *v21, a2: v38) == 0 )
                    break;
                  if ( (unsigned __int8)sub_140F80640(a1: v21[1], a2: v38, a3: 0) == 0 )
                    break;
                  v24 = v38[0];
                  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                    a1: v38[0],
                    a2: (__int64)v21 + 20,
                    a3: 2);
                  if ( *(_DWORD *)(v24 + 16) != 0 )
                    break;
                  v25 = v38[0];
                  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                    a1: v38[0],
                    a2: (__int64)v21 + 22,
                    a3: 2);
                  if ( *(_DWORD *)(v25 + 16) != 0 )
                    break;
                  v8 = (_DWORD *)v38[0];
                  if ( *(_DWORD *)(v38[0] + 16LL) != 0 )
                  {
                    LODWORD(v2) = 0;
                    if ( _InterlockedDecrement((volatile signed __int32 *)(v38[0] + 8LL)) == 0 )
                      goto LABEL_11;
                    return (unsigned int)v2;
                  }
                  ++v2;
                  v20 = *(_QWORD *)(a1 + 56);
                  if ( v2 >= (*(_QWORD *)(a1 + 64) - v20) >> 3 )
                    goto LABEL_38;
                }
              }
            }
          }
          else
          {
            v2 = 0;
            while ( 1 )
            {
              v11 = *(_QWORD *)(v10 + 8 * v2);
              LOBYTE(v37) = 0;
              v12 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v38[0] + 40LL))(
                a1: v38[0],
                a2: &v37,
                a3: 1);
              if ( *(_DWORD *)(v12 + 16) != 0 )
                break;
              v13 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                a1: v38[0],
                a2: v11 + 4,
                a3: 4);
              if ( *(_DWORD *)(v13 + 16) != 0 )
                break;
              v14 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                a1: v38[0],
                a2: v11 + 10,
                a3: 1);
              if ( *(_DWORD *)(v14 + 16) != 0 )
                break;
              v15 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(a1: v38[0], a2: v11, a3: 2);
              if ( *(_DWORD *)(v15 + 16) != 0 )
                break;
              v16 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                a1: v38[0],
                a2: v11 + 2,
                a3: 2);
              if ( *(_DWORD *)(v16 + 16) != 0 )
                break;
              v17 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                a1: v38[0],
                a2: v11 + 11,
                a3: 1);
              if ( *(_DWORD *)(v17 + 16) != 0 )
                break;
              v18 = v38[0];
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v38[0] + 40LL))(
                a1: v38[0],
                a2: v11 + 8,
                a3: 2);
              if ( *(_DWORD *)(v18 + 16) != 0 )
                break;
              ++v2;
              v10 = *(_QWORD *)(a1 + 32);
              if ( v2 >= (*(_QWORD *)(a1 + 40) - v10) >> 3 )
                goto LABEL_24;
            }
          }
        }
        LODWORD(v2) = 0;
LABEL_9:
        v8 = (_DWORD *)v38[0];
        if ( v38[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v38[0] + 8LL)) == 0 )
LABEL_11:
          (**(void (__fastcall ***)(_DWORD *, __int64))v8)(a1: v8, a2: 1);
        return (unsigned int)v2;
      }
    }
  }
  LODWORD(v2) = 0;
  return (unsigned int)v2;
}
