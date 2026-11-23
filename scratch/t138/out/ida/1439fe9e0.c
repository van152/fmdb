__int64 __fastcall sub_1439FE9E0(_QWORD *a1, _QWORD *a2)
{
  int v4; // r9d
  void (__fastcall ***v5)(_QWORD, __int64); // rcx
  __int64 v6; // rdi
  __int64 v7; // rdi
  __int64 v8; // rdi
  __int64 v9; // rdi
  unsigned int v10; // esi
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  __int64 v13; // rax
  unsigned __int64 v14; // rbx
  __int64 v15; // rdi
  __int64 v16; // rbx
  __int64 v17; // [rsp+30h] [rbp-20h] BYREF
  _BYTE v18[8]; // [rsp+38h] [rbp-18h] BYREF
  __int64 v19; // [rsp+40h] [rbp-10h] BYREF
  _QWORD v20[5]; // [rsp+48h] [rbp-8h] BYREF

  v20[1] = -2;
  sub_14080D0E0(a1: v18, a2: 0x1418E2C24LL);
  v17 = 0x80100004E554C4CLL;
  if ( *a2 != 0 )
  {
    (*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, _BYTE *))(*(_QWORD *)*a2 + 224LL))(
      a1: *a2,
      a2: &v19,
      a3: &qword_141B5B7B0,
      a4: v18);
    if ( v19 != 0 )
    {
      LOWORD(v4) = 5;
      sub_1407D1280(a1: (unsigned int)&v17, a2: (unsigned int)v20, a3: (unsigned int)&v19, a4: v4, a5: 0);
      v5 = (void (__fastcall ***)(_QWORD, __int64))v19;
      if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) == 0 )
        (**v5)(a1: v5, a2: 1);
      v6 = v20[0];
      if ( v20[0] != 0 )
      {
        (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v20[0] + 40LL))(
          a1: v20[0],
          a2: &dword_141AAB3AC,
          a3: 4);
        if ( *(_DWORD *)(v6 + 16) == 0 )
        {
          v7 = v20[0];
          (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v20[0] + 40LL))(
            a1: v20[0],
            a2: &dword_141AAB390,
            a3: 4);
          if ( *(_DWORD *)(v7 + 16) == 0 )
          {
            v8 = v20[0];
            (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)v20[0] + 40LL))(
              a1: v20[0],
              a2: &word_141B5B8E0,
              a3: 2);
            if ( *(_DWORD *)(v8 + 16) == 0 )
            {
              v9 = v20[0];
              LODWORD(v19) = (a1[6] - a1[5]) >> 3;
              (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v20[0] + 40LL))(
                a1: v20[0],
                a2: &v19,
                a3: 4);
              if ( *(_DWORD *)(v9 + 16) == 0 )
              {
                v13 = a1[5];
                if ( a1[6] == v13 )
                {
LABEL_21:
                  if ( (unsigned __int8)sub_140B4C6E0(a1, a2: v20) != 0 )
                  {
                    LODWORD(v19) = (*(_QWORD *)(*a1 + 8LL) - *(_QWORD *)*a1) >> 3;
                    v15 = v20[0];
                    (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v20[0] + 40LL))(
                      a1: v20[0],
                      a2: &v19,
                      a3: 4);
                    if ( *(_DWORD *)(v15 + 16) == 0 )
                    {
                      if ( (_DWORD)v19 == 0 )
                      {
LABEL_27:
                        v10 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(**(_QWORD **)(qword_141B5AD60 + 8) + 672LL))(
                                a1: *(_QWORD *)(qword_141B5AD60 + 8),
                                a2: v20);
                        goto LABEL_12;
                      }
                      v16 = 0;
                      while ( (unsigned __int8)sub_140B4C6E0(a1: *(_QWORD *)(*(_QWORD *)*a1 + 8 * v16), a2: v20) != 0 )
                      {
                        if ( ++v16 >= (unsigned __int64)(unsigned int)v19 )
                          goto LABEL_27;
                      }
                    }
                  }
                }
                else
                {
                  v14 = 0;
                  while ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(**(_QWORD **)(v13 + 8 * v14) + 248LL))(
                            a1: *(_QWORD *)(v13 + 8 * v14),
                            a2: v20) != 0 )
                  {
                    ++v14;
                    v13 = a1[5];
                    if ( v14 >= (a1[6] - v13) >> 3 )
                      goto LABEL_21;
                  }
                }
              }
            }
          }
        }
        v10 = 0;
LABEL_12:
        v11 = (void (__fastcall ***)(_QWORD, __int64))v20[0];
        if ( v20[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20[0] + 8LL)) == 0 )
          (**v11)(a1: v11, a2: 1);
        return v10;
      }
    }
  }
  return 0;
}
