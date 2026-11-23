__int64 sub_14377E370()
{
  __int64 result; // rax

  result = qword_141B5A490;
  if ( qword_141B5A490 == 0 )
  {
    if ( dword_141B5A48C > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5A48C);
      if ( dword_141B5A48C == -1 )
      {
        sub_140840620();
        sub_141751048(sub_1408407C0);
        sub_141750EA0(&dword_141B5A48C);
      }
    }
    result = qword_141B5A490;
    if ( qword_141B5A490 == 0 )
    {
      byte_141B5A498 = 1;
      result = sub_141750CC0(216);
      *(_OWORD *)(result + 32) = 0;
      *(_OWORD *)(result + 16) = 0;
      *(_OWORD *)(result + 48) = 0;
      *(_OWORD *)(result + 64) = 0;
      *(_OWORD *)(result + 80) = 0;
      *(_OWORD *)(result + 96) = 0;
      *(_OWORD *)(result + 112) = 0;
      *(_OWORD *)(result + 128) = 0;
      *(_OWORD *)(result + 144) = 0;
      *(_OWORD *)(result + 160) = 0;
      *(_OWORD *)(result + 176) = 0;
      *(_OWORD *)(result + 192) = 0;
      *(_QWORD *)(result + 208) = 0;
      *(_QWORD *)result = 0x14185FC78LL;
      *(_QWORD *)(result + 8) = 0x14185FD28LL;
      *(_BYTE *)(result + 32) = 3;
      *(_QWORD *)(result + 24) = 0x14185FE68LL;
      *(_BYTE *)(result + 48) = 1;
      *(_QWORD *)(result + 40) = 0x14185FFA8LL;
      *(_BYTE *)(result + 64) = 2;
      *(_QWORD *)(result + 56) = 0x1418600E8LL;
      *(_BYTE *)(result + 80) = 15;
      *(_QWORD *)(result + 72) = 0x141860228LL;
      *(_BYTE *)(result + 96) = 24;
      *(_QWORD *)(result + 88) = 0x141860368LL;
      *(_BYTE *)(result + 112) = 25;
      *(_QWORD *)(result + 104) = 0x1418604A8LL;
      *(_BYTE *)(result + 128) = 5;
      *(_QWORD *)(result + 120) = 0x1418605E8LL;
      *(_BYTE *)(result + 144) = 26;
      *(_QWORD *)(result + 136) = 0x141860728LL;
      *(_BYTE *)(result + 160) = 14;
      *(_QWORD *)(result + 152) = 0x141860868LL;
      *(_BYTE *)(result + 176) = 11;
      *(_QWORD *)(result + 168) = 0x1418609A8LL;
      *(_BYTE *)(result + 192) = 10;
      *(_QWORD *)(result + 184) = 0x141860AE8LL;
      *(_BYTE *)(result + 208) = 27;
      *(_QWORD *)(result + 200) = 0x141860C68LL;
      qword_141B5A490 = result;
      byte_141B5A498 = 0;
    }
  }
  return result;
}
