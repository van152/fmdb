__int64 __fastcall sub_144139840(__int64 a1, char a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  _QWORD v6[4]; // [rsp+20h] [rbp-10h] BYREF

  v6[2] = -2;
  *(_QWORD *)a1 = 0x141897B58LL;
  *(_BYTE *)(a1 + 8) = a2;
  if ( dword_141B62768 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B62768);
    if ( dword_141B62768 == -1 )
    {
      v4 = qword_141ABD470;
      if ( qword_141ABD470 == 0 )
      {
        v4 = sub_1407E4940();
        qword_141ABD470 = v4;
      }
      qword_141B62760 = 0;
      qword_141B62758 = 0;
      v5 = sub_1407E4490(v4, 48);
      *(_QWORD *)v5 = v5;
      *(_QWORD *)(v5 + 8) = v5;
      *(_QWORD *)(v5 + 16) = v5;
      *(_WORD *)(v5 + 24) = 257;
      qword_141B62758 = v5;
      sub_141751048(sub_1412EAE20);
      sub_141750EA0(&dword_141B62768);
    }
  }
  sub_1412EAF00(&qword_141B62758, v6, a1 + 8);
  *(_QWORD *)(v6[0] + 40LL) = a1;
  return a1;
}
