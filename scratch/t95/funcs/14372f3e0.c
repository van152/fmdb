__int64 __fastcall sub_14372F3E0(__int64 a1, unsigned int a2, _QWORD *a3, char a4)
{
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 **v11; // rcx
  __int64 *v12; // rax
  __int64 *v13; // r8
  __int64 ***v14; // r9
  __int64 **v15; // rbp
  __int64 **v16; // rdi
  __int64 v17; // rcx
  __int64 v18; // rbx
  __int64 v19; // rsi
  __int64 v20; // rdx
  __int64 v22; // [rsp+28h] [rbp-50h] BYREF
  __int64 v23; // [rsp+30h] [rbp-48h] BYREF
  _QWORD v24[8]; // [rsp+38h] [rbp-40h] BYREF

  v8 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*a3 + 8LL))(*a3);
  sub_14081D8D0(v24, v8, a2);
  v9 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*a3 + 16LL))(*a3);
  sub_14081D8D0(&v23, v9, a2);
  v10 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*a3 + 24LL))(*a3);
  sub_14081D8D0(&v22, v10, a2);
  v11 = *(__int64 ***)(a1 + 16);
  if ( v11 != nullptr )
  {
    v12 = *v11;
    v13 = v11[1];
    while ( v12 != v13 )
    {
      v14 = (__int64 ***)*v12;
      if ( *(_DWORD *)(*v12 + 24) != 0 )
      {
        v15 = *v14;
        v16 = v14[1];
        while ( v15 != v16 )
        {
          if ( v15[1] == nullptr )
          {
            v17 = **v15;
            v18 = v22;
            if ( v24[0] == v17 || v22 == v17 || v23 == v17 )
            {
              v19 = (*v15)[2];
              if ( v19 != 0 )
              {
                v20 = *a3;
                if ( *a3 != 0 )
                {
                  v15[1] = (__int64 *)v20;
                  _InterlockedIncrement((volatile signed __int32 *)(v20 + 8));
                }
                --*((_DWORD *)v14 + 6);
                *(_BYTE *)(v19 + 84) = a4;
                if ( v18 == v17 )
                  ++*((_DWORD *)v14 + 7);
              }
            }
          }
          v15 += 2;
        }
      }
      ++v12;
    }
  }
  return a1;
}
